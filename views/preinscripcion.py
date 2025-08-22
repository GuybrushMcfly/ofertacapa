import streamlit as st
import pandas as pd
import random
from datetime import date
from modules.db import (
    get_supabase_client,
    validar_cuil,
    verificar_formulario_cuil,
    verificar_formulario_historial,
    verificar_formulario_comision,
    obtener_datos_para_formulario,
    insertar_inscripcion,
    obtener_comisiones_abiertas
)

# ==========================================================
# CONEXIÓN A SUPABASE
# ==========================================================
supabase = get_supabase_client()


# ==========================================================
# DIÁLOGO DE ÉXITO (modal al inscribirse)
# ==========================================================
@st.dialog("✅ ¡Preinscripción exitosa!", width="large", dismissible=False)
def mostrar_dialogo_exito():
    actividad = st.session_state.get("actividad_nombre", "la actividad seleccionada")
    datos_agente = st.session_state.get("datos_agenteform", {})
    
    # Tomamos solo el nombre (si existe en los datos del agente)
    nombre = datos_agente.get("nombre", "Agente")

    st.markdown(f"""
    <div style="
        background-color:#f0f8ff;
        border-left: 6px solid #136ac1;
        border-radius:10px;
        padding:20px;
        text-align:center;
        font-size:17px;">
        <b>{nombre}</b>, tu preinscripción en la actividad 
        <b><span style="color:#136ac1;">{actividad}</span></b> fue registrada correctamente. 🎉
        <br><br>
        <span style="color:#555;">ℹ️ Recordá que esta solicitud no implica la asignación de vacante.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Cerrar"):
        st.session_state.clear()
        st.session_state["__reset_placeholder"] = True
        st.rerun()




# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================
def mostrar():
    # ==================== ESTILO GENERAL ====================
    st.markdown(
        """
        <style>
        .main-container {
            max-width: 70%;   /* ancho máximo */
            margin: 0 auto;   /* centrado horizontal */
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 🔹 Abrir contenedor centrado
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # -------------------------
    # PASO 1: Traer comisiones
    # -------------------------
    st.markdown("## 📝 Formulario de Preinscripción")
    df_temp = pd.DataFrame(obtener_comisiones_abiertas(supabase))
    if df_temp.empty:
        st.warning("No hay comisiones disponibles actualmente.")
        st.markdown("</div>", unsafe_allow_html=True)   # cerrar div
        return

    # -------------------------
    # PASO 2: Selección
    # -------------------------
    st.markdown("##### 2) Seleccioná la actividad en la cual querés preinscribirte.")
    df_temp["Actividad (Comisión)"] = df_temp["nombre_actividad"] + " (" + df_temp["id_comision_sai"] + ")"
    dropdown_list = ["-Seleccioná una actividad para preinscribirte-"] + df_temp["Actividad (Comisión)"].tolist()

    selected_from_query = st.query_params.get("selected_activity", [None])[0]
    initial_index = dropdown_list.index(selected_from_query) if selected_from_query in dropdown_list else 0
    clave_selectbox = f"actividad_key_{random.randint(0,999999)}" if st.session_state.get("__reset_placeholder") else "actividad_key_default"

    actividad_seleccionada = st.selectbox("Actividad disponible", dropdown_list, index=initial_index, key=clave_selectbox)

    if actividad_seleccionada not in dropdown_list:
        actividad_seleccionada = dropdown_list[0]

    # Reset tras éxito
    if st.session_state.get("__reset_placeholder", False):
        st.session_state["__reset_placeholder"] = False
        st.session_state["actividad_anterior"] = "-Seleccioná una actividad para preinscribirte-"

    if "actividad_anterior" not in st.session_state:
        st.session_state["actividad_anterior"] = ""

    if actividad_seleccionada != st.session_state["actividad_anterior"]:
        st.session_state["actividad_anterior"] = actividad_seleccionada
        st.session_state["cuil_valido"] = False
        st.session_state["validado"] = False
        st.session_state["cuil"] = ""
        st.session_state["datos_agenteform"] = {}

    if actividad_seleccionada != "-Seleccioná una actividad para preinscribirte-":
        fila = df_temp[df_temp["Actividad (Comisión)"] == actividad_seleccionada].iloc[0]
        st.session_state["actividad_nombre"] = fila["nombre_actividad"]
        st.session_state["comision_nombre"] = fila["id_comision_sai"]
        st.session_state["fecha_inicio"] = fila["fecha_desde"]
        st.session_state["fecha_fin"] = fila["fecha_hasta"]
        
        # Debug para ver qué columnas y datos hay realmente
        st.write("👉 Columnas del DataFrame:", df_temp.columns.tolist())
        st.write("👉 Fila seleccionada:", fila.to_dict())
        
        # Ahora usamos id si existe, si no usamos id_comision_sai
        if "id" in fila:
            st.session_state["comision_id"] = fila["id"]
        else:
            st.session_state["comision_id"] = fila["id_comision_sai"]
        
        st.session_state["id_actividad"] = fila["id_actividad"]


        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 15px; border-left: 5px solid #136ac1; border-radius: 5px;">
          <b>🟦 Actividad:</b> {fila['nombre_actividad']}<br>
          <b>🆔 Comisión:</b> {fila['id_comision_sai']}<br>
          <b>🧬 UUID Comisión:</b> <code>{fila['id']}</code><br>
          <b>📅 Fechas:</b> {fila['fecha_desde']} al {fila['fecha_hasta']}<br>
          <b>📌 Cierre Inscripción:</b> {fila['fecha_cierre']}<br>
          <b>⭐ Créditos:</b> {fila['creditos']}<br>
          <b>🎓 Modalidad:</b> {fila['modalidad_cursada']}<br>
          <b>❓ Apto tramo:</b> {fila['apto_tramo']}<br>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # PASO 3: Validación CUIL
    # -------------------------
    if actividad_seleccionada != "-Seleccioná una actividad para preinscribirte-":
        st.markdown("##### 3) Ingresá tu número de CUIL y validalo con el botón.")
        cuil_input = st.text_input("CUIL (11 dígitos)", max_chars=11)

        if st.button("Validar CUIL"):
            if not validar_cuil(cuil_input):
                st.error("CUIL inválido. Verificá que tenga 11 dígitos y sea correcto.")
                return
            if not verificar_formulario_cuil(supabase, cuil_input):
                st.error("⚠️ El CUIL no corresponde a un agente activo.")
                return
            if verificar_formulario_historial(supabase, cuil_input, st.session_state["id_actividad"]):
                st.warning("⚠️ Ya realizaste esta actividad y fue APROBADA.")
                return
            if verificar_formulario_comision(supabase, cuil_input, st.session_state["comision_id"]):
                st.warning("⚠️ Ya estás inscripto en esta comisión.")
                return

            st.session_state["cuil"] = cuil_input
            st.session_state["cuil_valido"] = True
            st.session_state["validado"] = True
            st.success("✅ CUIL válido. Podés completar el formulario.")
            st.session_state["datos_agenteform"] = obtener_datos_para_formulario(supabase, cuil_input)

            datos = st.session_state["datos_agenteform"]
            if datos:
                st.markdown("### 👤 Datos obtenidos del agente")
                st.json(datos)

    # -------------------------
    # PASO 4: Formulario final
    # -------------------------
    if (
        st.session_state.get("validado")
        and st.session_state.get("cuil_valido")
        and not st.session_state.get("inscripcion_exitosa")
    ):
        datos = st.session_state["datos_agenteform"]
        correo_oficial = datos.get("email", "")
        tareas = st.text_area("✍️ Tareas desarrolladas (obligatorio)", height=120).strip().lower()
        st.markdown(f"📧 Te vamos a contactar al correo registrado: **{correo_oficial}**")
        email_alt = st.text_input("Correo alternativo (opcional)").strip()

        if st.button("ENVIAR INSCRIPCIÓN"):
            if not tareas:
                st.error("⚠️ El campo 'Tareas desarrolladas' es obligatorio.")
                return
            if email_alt and "@" not in email_alt:
                st.error("⚠️ Correo alternativo inválido.")
                return

            edad = None
            if datos.get("fecha_nacimiento"):
                try:
                    fecha_nac = pd.to_datetime(datos["fecha_nacimiento"])
                    hoy = pd.Timestamp.today()
                    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
                except:
                    pass

            datos_inscripcion = {
                "comision_id": st.session_state["comision_id"],
                "cuil": st.session_state["cuil"],
                "fecha_inscripcion": date.today().isoformat(),
                "estado_inscripcion": "Nueva",
                "vacante": False,
                "tareas_desarrolladas": tareas,
                "email": correo_oficial,
                "email_alternativo": email_alt if email_alt else None,
                "fecha_nacimiento": datos.get("fecha_nacimiento"),
                "edad_inscripcion": edad,
                "titulo": datos.get("titulo"),
                "nivel_educativo": datos.get("nivel_educativo"),
                "sexo": datos.get("sexo"),
                "situacion_revista": datos.get("situacion_revista"),
                "nivel": datos.get("nivel"),
                "grado": datos.get("grado"),
                "agrupamiento": datos.get("agrupamiento"),
                "tramo": datos.get("tramo"),
                "id_dependencia_simple": datos.get("id_dependencia_simple"),
                "id_dependencia_general": datos.get("id_dependencia_general"),
            }

            result = insertar_inscripcion(supabase, datos_inscripcion)
            if result.data:
                st.session_state["inscripcion_exitosa"] = True
                mostrar_dialogo_exito()
            else:
                st.error("❌ Ocurrió un error al guardar la inscripción.")

    # 🔹 Cerrar contenedor centrado
    st.markdown("</div>", unsafe_allow_html=True)
