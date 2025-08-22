import streamlit as st
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
from datetime import datetime

supabase = get_supabase_client()

def mostrar():
    st.markdown("## 📝 Formulario de Preinscripción")

    # 1️⃣ Cargar comisiones disponibles
    comisiones = obtener_comisiones_abiertas(supabase)
    if not comisiones:
        st.warning("No hay comisiones abiertas en este momento.")
        return

    opciones_dropdown = ["-Seleccioná una actividad-"] + [
        f"{c['nombre_actividad']} ({c['id_comision_sai']})" for c in comisiones
    ]
    seleccion = st.selectbox("Actividad disponible", opciones_dropdown)

    if seleccion == "-Seleccioná una actividad-":
        st.stop()

    fila = next((c for c in comisiones if f"{c['nombre_actividad']} ({c['id_comision_sai']})" == seleccion), None)
    if not fila:
        st.error("No se encontró la actividad seleccionada.")
        return

    actividad_id = fila["id_actividad"]
    comision_id = fila["id_comision_sai"]

    st.markdown("""
        <div style='border-left: 5px solid #136ac1; padding: 10px; background-color: #f0f8ff;'>
            <b>Organiza:</b> {0}<br>
            <b>Fechas:</b> {1} al {2}<br>
            <b>Modalidad:</b> {3}<br>
            <b>Créditos:</b> {4}
        </div>
    """.format(
        fila.get("organismo", ""),
        fila.get("fecha_desde", ""),
        fila.get("fecha_hasta", ""),
        fila.get("modalidad_cursada", ""),
        fila.get("creditos", "")
    ), unsafe_allow_html=True)

    # 2️⃣ Ingreso y validación de CUIL
    cuil_input = st.text_input("Ingresá tu CUIL (11 dígitos)", max_chars=11)

    if st.button("Validar CUIL"):
        if not validar_cuil(cuil_input):
            st.error("CUIL inválido. Verificá que tenga 11 dígitos.")
            st.stop()

        existe = verificar_formulario_cuil(supabase, cuil_input).data
        if not existe:
            st.error("El CUIL no corresponde a un agente activo.")
            st.stop()

        ya_aprobo = verificar_formulario_historial(supabase, cuil_input, actividad_id).data
        if ya_aprobo:
            st.warning("Ya aprobaste esta actividad previamente.")
            st.stop()

        ya_inscripto = verificar_formulario_inscripcion(supabase, cuil_input, comision_id).data
        if ya_inscripto:
            st.warning("Ya estás inscripto en esta comisión.")
            st.stop()

        st.session_state["validado"] = True
        st.session_state["cuil"] = cuil_input

    if st.session_state.get("validado"):
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
                    st.stop()

                datos_inscripcion = {
                    "cuil": st.session_state["cuil"],
                    "id_actividad": actividad_id,
                    "id_comision": comision_id,
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
