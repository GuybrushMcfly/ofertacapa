import streamlit as st
import pandas as pd
from datetime import date, datetime
import random
from modules.db import (
    get_supabase_client,
    verificar_formulario_cuil,
    verificar_formulario_historial,
    verificar_formulario_comision,
    obtener_datos_para_formulario,
    insertar_inscripcion,
    obtener_comisiones_abiertas
)

# ========== CONEXIÓN ==========
supabase = get_supabase_client()

# ========== RESET GLOBAL ==========
if st.session_state.get("inscripcion_exitosa", False):
    st.balloons()
    st.success("✅ ¡Preinscripción exitosa! Tus datos fueron enviados correctamente.")
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()

# ========== OBTENER DATOS ==========
df_temp = pd.DataFrame(obtener_comisiones_abiertas(supabase))
if df_temp.empty:
    st.warning("No hay actividades disponibles para preinscripción.")
    st.stop()

# ========== CAMPOS VISUALES ==========
df_temp["Fecha inicio"] = pd.to_datetime(df_temp["fecha_desde"]).dt.strftime("%d/%m/%Y")
df_temp["Fecha fin"] = pd.to_datetime(df_temp["fecha_hasta"]).dt.strftime("%d/%m/%Y")
df_temp["Actividad (Comisión)"] = df_temp["nombre_actividad"] + " (" + df_temp["id_comision_sai"] + ")"

# ========== PASO 1: SELECCIÓN ==========
st.markdown("## 📝 Formulario de Preinscripción")
dropdown_list = ["-Seleccioná una actividad para preinscribirte-"] + df_temp["Actividad (Comisión)"].tolist()

selected_from_query = st.query_params.get("selected_activity", [None])[0]
initial_index = dropdown_list.index(selected_from_query) if selected_from_query in dropdown_list else 0

clave_selectbox = f"actividad_key_{random.randint(0, 999999)}" if st.session_state.get("__reset_placeholder") else "actividad_key_default"
actividad_seleccionada = st.selectbox("Actividad disponible", dropdown_list, index=initial_index, key=clave_selectbox)

if actividad_seleccionada == dropdown_list[0]:
    st.stop()

fila = df_temp[df_temp["Actividad (Comisión)"] == actividad_seleccionada].iloc[0]
st.markdown(f"""
<div style='border-left: 5px solid #136ac1; background-color: #f0f8ff; padding: 12px;'>
    <b>Actividad:</b> {fila['nombre_actividad']}<br>
    <b>Organismo:</b> {fila['organismo']}<br>
    <b>Comisión:</b> {fila['id_comision_sai']}<br>
    <b>Fecha inicio:</b> {fila['Fecha inicio']} | <b>Fecha fin:</b> {fila['Fecha fin']}<br>
    <b>Modalidad:</b> {fila['modalidad_cursada']}<br>
    <b>Créditos:</b> {fila['creditos']}
</div>
""", unsafe_allow_html=True)

# ========== PASO 2: VALIDACIÓN CUIL ==========
cuil_input = st.text_input("CUIL (11 dígitos)", max_chars=11)

if st.button("Validar CUIL"):
    if not cuil_input.isdigit() or len(cuil_input) != 11:
        st.error("CUIL inválido. Debe tener 11 dígitos.")
        st.stop()

    actividad_id = fila["id_actividad"]
    comision_id = fila["id"]

    if not verificar_formulario_cuil(supabase, cuil_input):
        st.error("El CUIL no corresponde a un agente activo.")
        st.stop()

    if verificar_formulario_historial(supabase, cuil_input, actividad_id):
        st.warning("Ya aprobaste esta actividad previamente.")
        st.stop()

    if verificar_formulario_comision(supabase, cuil_input, comision_id):
        st.warning("Ya estás inscripto en esta comisión.")
        st.stop()

    st.session_state["cuil"] = cuil_input
    st.session_state["validado"] = True
    st.session_state["comision_id"] = comision_id
    st.session_state["id_actividad"] = actividad_id

# ========== PASO 3: FORMULARIO ==========
if st.session_state.get("validado"):
    datos = obtener_datos_para_formulario(supabase, st.session_state["cuil"])
    correo_oficial = datos.get("email", "")
    nombre_agente = f"{datos.get('nombre', '')} {datos.get('apellido', '')}".strip()

    st.markdown(f"### 👤 {nombre_agente}")
    st.markdown("Completá los siguientes campos para finalizar tu preinscripción:")

    col1, col2 = st.columns(2)
    niveles = [
        "-Seleccioná último nivel completo-", "PRIMARIO", "SECUNDARIO",
        "TERCIARIO", "UNIVERSITARIO", "POSGRADO"
    ]
    nivel_val = datos.get("nivel_educativo", "")
    index_nivel = niveles.index(nivel_val) if nivel_val in niveles else 0

    with col1:
        nivel_educativo = st.selectbox("Nivel educativo", niveles, index=index_nivel)
    with col2:
        titulo = st.text_input("Título", value=datos.get("titulo", "")).upper()

    tareas = st.text_area("Tareas desarrolladas", height=100).lower()
    st.markdown(f"📧 Correo registrado: **{correo_oficial}**")
    email_alt = st.text_input("Correo alternativo (opcional)")

    if st.form_submit_button("Enviar inscripción") if 'form_submit_button' in dir(st) else st.button("Enviar inscripción"):
        if email_alt and "@" not in email_alt:
            st.error("Correo alternativo inválido.")
            st.stop()

        fecha_nac = pd.to_datetime(datos.get("fecha_nacimiento")) if datos.get("fecha_nacimiento") else None
        hoy = pd.Timestamp.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day)) if fecha_nac else None

        datos_insc = {
            "comision_id": st.session_state["comision_id"],
            "cuil": st.session_state["cuil"],
            "fecha_inscripcion": date.today().isoformat(),
            "estado_inscripcion": "Nueva",
            "vacante": False,
            "nivel_educativo": nivel_educativo if nivel_educativo != "-Seleccioná último nivel completo-" else None,
            "titulo": titulo,
            "tareas_desarrolladas": tareas,
            "email": correo_oficial,
            "email_alternativo": email_alt,
            "fecha_nacimiento": datos.get("fecha_nacimiento"),
            "edad_inscripcion": edad,
            "sexo": datos.get("sexo"),
            "situacion_revista": datos.get("situacion_revista"),
            "nivel": datos.get("nivel"),
            "grado": datos.get("grado"),
            "agrupamiento": datos.get("agrupamiento"),
            "tramo": datos.get("tramo"),
            "id_dependencia_simple": datos.get("id_dependencia_simple"),
            "id_dependencia_general": datos.get("id_dependencia_general")
        }

        res = insertar_inscripcion(supabase, datos_insc)
        if res.data:
            st.session_state["inscripcion_exitosa"] = True
            st.rerun()
        else:
            st.error("Error al registrar la inscripción.")
