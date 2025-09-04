import streamlit as st
import time
import pandas as pd
import random
from datetime import date
from modules.db import (
    get_supabase_client,
    validar_cuil,
    obtener_datos_para_formulario,
    insertar_inscripcion,
    obtener_comisiones_abiertas,
    verificar_preinscripcion   
)

from modules.utils import formatear_fecha

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
        <br><br>
        <span style="color:#555;">🚨🚨 Si es un curso de INAP, acordate de inscribirte también en su página. 🚨🚨</span>      
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Cerrar", type="primary"):
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
        /* Acá podés agregar estilos generales si querés */
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # PASO 1: Traer comisiones
    # -------------------------
    st.markdown(
        "<h4 style='text-align: center; color: #136ac1;'>📝 PREINSCRIPCIÓN EN ACTIVIDADES DE CAPACITACIÓN</h4>",
        unsafe_allow_html=True
    )

    df_temp = pd.DataFrame(obtener_comisiones_abiertas(supabase))
    if df_temp.empty:
        st.warning("No hay comisiones disponibles actualmente.")
        return

    # -------------------------
    # PASO 2: Selección
    # -------------------------
    st.markdown("###### 1) 🔎 Seleccioná la actividad en la cual querés preinscribirte.")
    
    df_temp["Actividad (Comisión)"] = df_temp["nombre_actividad"] + " (" + df_temp["id_comision_sai"] + ")"
    
    # 🔹 Ordenar actividades alfabéticamente
    actividades_ordenadas = sorted(df_temp["Actividad (Comisión)"].tolist(), key=str.lower)
    
    # 🔹 Armar lista final con el placeholder arriba
    dropdown_list = ["-Seleccioná una actividad para preinscribirte-"] + actividades_ordenadas

    selected_from_query = st.query_params.get("selected_activity", [None])[0]
    initial_index = dropdown_list.index(selected_from_query) if selected_from_query in dropdown_list else 0
    clave_selectbox = f"actividad_key_{random.randint(0,999999)}" if st.session_state.get("__reset_placeholder") else "actividad_key_default"

    actividad_seleccionada = st.selectbox("", dropdown_list, index=initial_index, key=clave_selectbox)

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
        st.session_state["comision_id"] = fila["id"]
        st.session_state["id_actividad"] = fila["id_actividad"]

        # 🔹 Formatear fechas con utils
        fecha_inicio = formatear_fecha(pd.to_datetime(fila["fecha_desde"]))
        fecha_fin = formatear_fecha(pd.to_datetime(fila["fecha_hasta"]))
        fecha_cierre = formatear_fecha(pd.to_datetime(fila["fecha_cierre"]))

        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 15px; border-left: 5px solid #136ac1; border-radius: 5px;">
          <b>🆔 Comisión:</b> {fila['id_comision_sai']}<br>
          <b>🏫 Organismo:</b> {fila['organismo']}<br>
          <b>📅 Cursada:</b> {fecha_inicio} al {fecha_fin}<br>
          <b>📅 Cierre Inscripción:</b> {fecha_cierre}<br>
          <b>⭐ Créditos:</b> {fila['creditos']}<br>
          <b>🎓 Modalidad:</b> {fila['modalidad_cursada']}<br>
          <b>➡️ Apto tramo:</b> {fila['apto_tramo']}<br>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # PASO 3: Validación CUIL
    # -------------------------
    if actividad_seleccionada != "-Seleccioná una actividad para preinscribirte-":
        st.markdown("---")
        st.markdown("###### 2) 🆔 Ingresá tu número de CUIL/CUIT y validalo con el botón.")
                
      #  cuil_input = st.text_input("CUIL/CUIT (11 dígitos)", max_chars=11)
        col1, col2, col3 = st.columns([1,1,1])  # 3 columnas iguales
        with col1:
            cuil_input = st.text_input("CUIL/CUIT (11 dígitos)", max_chars=11)
        

        #if st.button("Validar CUIL/CUIT"):
        if st.button("Validar CUIL/CUIT", type="primary"):
            if not validar_cuil(cuil_input):
                st.error("🚨 CUIL/CUIT inválido. Verificá que tenga 11 dígitos y sea correcto.")
                return
        
            datos_check = verificar_preinscripcion(
                supabase,
                cuil_input,
                st.session_state["id_actividad"],
                st.session_state["comision_id"]
            )
        
            if not datos_check.get("existe_agente", False):
                st.error("🚨 El CUIL/CUIT no corresponde a un agente activo.")
                return
            if datos_check.get("ya_aprobo", False):
                st.info("⚠️ Ya aprobaste esta actividad anteriormente.")
                return
            if datos_check.get("ya_inscripto", False):
                st.info("⚠️ Ya realizaste la preinscripción en esta comisión. No es necesario volver a realizarla.")
                return
        
            # ✅ Si todo OK
            st.session_state["cuil"] = cuil_input
            st.session_state["cuil_valido"] = True
            st.session_state["validado"] = True
            st.success("✅ CUIL/CUIT válido. Podés continuar con la preinscripción.")
            st.session_state["datos_agenteform"] = obtener_datos_para_formulario(supabase, cuil_input)

            
            # Ajustes de valores por defecto
            datos = st.session_state["datos_agenteform"]
            if not datos.get("nivel_educativo") or str(datos.get("nivel_educativo")).upper() == "NULL":
                datos["nivel_educativo"] = "SECUNDARIO"
            if not datos.get("titulo") or str(datos.get("titulo")).upper() == "NULL":
                datos["titulo"] = "SIN DATOS"
            st.session_state["datos_agenteform"] = datos

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
        
        st.markdown("---")
        st.markdown("###### 3) 💻 Completá las tareas que desarrollás habitualmente.")
        tareas = st.text_area("✍️ Tareas desarrolladas (obligatorio)", height=120).strip().lower()
        st.markdown(f"📧 Por defecto, siempre te vamos a contactar al correo registrado: **{correo_oficial}**. Si necesitás agregar una forma de contacto adicional, completá el siguiente campo.")
       # email_alt = st.text_input("Correo alternativo (opcional)").strip()
        col1, col2, col3 = st.columns([1,1,1])  # 3 columnas iguales
        with col1:
            email_alt = st.text_input("Correo alternativo (opcional)").strip()
        

        if st.button("ENVIAR PREINSCRIPCIÓN", type="primary"):
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

       #     result = insertar_inscripcion(supabase, datos_inscripcion)
       #     if result.data:
       #         st.session_state["inscripcion_exitosa"] = True
       #         mostrar_dialogo_exito()
       #     else:
       #         st.error("❌ Ocurrió un error al guardar la inscripción.")

            result = insertar_inscripcion(supabase, datos_inscripcion)
            st.write("DEBUG RESULT:", result)  # Temporal para debugging
            
            if result is not None and "id" in result:
                st.session_state["inscripcion_exitosa"] = True
                mostrar_dialogo_exito()
            else:
                st.error("❌ Ocurrió un error al guardar la inscripción.")
                st.write("DEBUG: result =", result)
                
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.write("DEBUG EXCEPTION:", e)

