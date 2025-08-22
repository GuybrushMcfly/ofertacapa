import streamlit as st
import pandas as pd
from datetime import date, datetime
from modules.db import (
    get_supabase_client,
    verificar_formulario_cuil,
    verificar_formulario_historial,
    verificar_formulario_inscripcion,
    obtener_datos_para_formulario,
    insertar_inscripcion,
    obtener_comisiones_abiertas
)
from modules.utils import validar_cuil, validar_email, normalizar_titulo

supabase = get_supabase_client()

# ========== PREINSCRIPCIÓN ==========
def mostrar():
    st.markdown("## 📝 Formulario de Preinscripción")

    # 1️⃣ Cargar comisiones disponibles
    df_temp = pd.DataFrame(obtener_comisiones_abiertas(supabase))

    if df_temp.empty:
        st.warning("No hay comisiones disponibles actualmente.")
        return

    # 2️⃣ Dropdown de selección de actividad (combinada)
    df_temp["Actividad dropdown"] = df_temp["nombre_actividad"] + " (" + df_temp["id_comision_sai"] + ")"
    dropdown_list = ["-Seleccioná una actividad para preinscribirte-"] + df_temp["Actividad dropdown"].tolist()

    actividad_seleccionada = st.selectbox("Actividad disponible", dropdown_list)
    if actividad_seleccionada == dropdown_list[0]:
        return

    fila = df_temp[df_temp["Actividad dropdown"] == actividad_seleccionada].iloc[0]

    st.markdown("""
    <div style='border-left: 5px solid #136ac1; background-color: #f0f8ff; padding: 12px; margin-top: 10px;'>
        <b>Actividad:</b> {0}<br>
        <b>Organismo:</b> {1}<br>
        <b>Comisión:</b> {2}<br>
        <b>Fecha inicio:</b> {3} | <b>Fecha fin:</b> {4}<br>
        <b>Modalidad:</b> {5}<br>
        <b>Créditos:</b> {6}
    </div>
    """.format(
        fila["nombre_actividad"],
        fila["organismo"],
        fila["id_comision_sai"],
        fila["fecha_desde"],
        fila["fecha_hasta"],
        fila["modalidad_cursada"],
        fila["creditos"]
    ), unsafe_allow_html=True)

    # 3️⃣ Validación del CUIL
    cuil_input = st.text_input("CUIL (11 dígitos)")

    if st.button("Validar CUIL"):
        if not validar_cuil(cuil_input):
            st.error("CUIL inválido. Debe tener 11 dígitos.")
            return

        try:
            actividad_id = fila["id_actividad"]
            comision_id = fila["id_comision_sai"]

            st.write("🔎 Debug actividad_id:", actividad_id)
            st.write("🔎 Debug cuil_input:", cuil_input)

            existe = verificar_formulario_cuil(supabase, cuil_input).data
            if not existe:
                st.error("El CUIL no corresponde a un agente activo.")
                return

            ya_aprobo = verificar_formulario_historial(supabase, cuil_input, actividad_id).data
            if ya_aprobo:
                st.warning("Ya aprobaste esta actividad previamente.")
                return

            ya_inscripto = verificar_formulario_inscripcion(supabase, cuil_input, comision_id).data
            if ya_inscripto:
                st.warning("Ya estás inscripto en esta comisión.")
                return

            st.session_state["cuil_validado"] = True
            st.session_state["cuil"] = cuil_input
            st.session_state["actividad_id"] = actividad_id
            st.session_state["comision_id"] = comision_id

        except Exception as e:
            st.error(f"⚠️ Error al validar datos: {e}")
            return

    # 4️⃣ Mostrar formulario si está validado
    if st.session_state.get("cuil_validado"):
        datos = obtener_datos_para_formulario(supabase, st.session_state["cuil"]).data or {}

        with st.form("formulario_preinscripcion"):
            st.markdown("### ✍️ Completá los siguientes datos")

            nivel_educativo = st.selectbox("Nivel educativo", [
                "Primario completo", "Secundario completo", "Terciario", "Universitario", "Posgrado"
            ], index=0)

            titulo = st.text_input("Título alcanzado", value="")
            tareas = st.text_area("Tareas desarrolladas", height=100)
            correo_alternativo = st.text_input("Correo alternativo")

            submitted = st.form_submit_button("Confirmar preinscripción")

            if submitted:
                if not validar_email(correo_alternativo):
                    st.error("Correo alternativo inválido.")
                    return

                datos_inscripcion = {
                    "cuil": st.session_state["cuil"],
                    "id_actividad": st.session_state["actividad_id"],
                    "id_comision": st.session_state["comision_id"],
                    "nivel_educativo": nivel_educativo,
                    "titulo": normalizar_titulo(titulo),
                    "tareas": tareas.lower().strip(),
                    "correo_alternativo": correo_alternativo,
                    "fecha": datetime.now().isoformat(),
                    "estado": "PREINSCRIPTO"
                }

                resp = insertar_inscripcion(supabase, datos_inscripcion)
                if resp.data:
                    st.success("✅ ¡Preinscripción exitosa!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Error al registrar la inscripción. Intentá nuevamente.")
