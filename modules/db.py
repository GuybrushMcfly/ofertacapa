
# modules/db.py
import os
import streamlit as st
from supabase import create_client, Client

# ============================
# Conexión cacheada a Supabase
# ============================
@st.cache_resource
def get_supabase_client() -> Client:
    """
    Devuelve un cliente de Supabase cacheado en memoria
    """
    url = os.environ.get("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_ANON_KEY") or st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

# ============================
# RPCs de validación
# ============================
def validar_cuil(cuil: str) -> bool:
    if not cuil.isdigit() or len(cuil) != 11:
        return False
    mult = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(cuil[i]) * mult[i] for i in range(10))
    verificador = 11 - (total % 11)
    if verificador == 11: verificador = 0
    elif verificador == 10: verificador = 9
    return verificador == int(cuil[-1])

def verificar_formulario_cuil(supabase: Client, cuil: str) -> bool:
    try:
        response = supabase.rpc("verificar_formulario_cuil", {"cuil_input": cuil}).execute()
        return response.data[0].get("existe", False)
    except Exception:
        st.error("Error al verificar el CUIL en la base de datos.")
        return False

def verificar_formulario_historial(supabase: Client, cuil: str, id_actividad: str) -> bool:
    try:
        response = supabase.rpc("verificar_formulario_historial", {
            "cuil_input": cuil,
            "id_actividad_input": id_actividad
        }).execute()
        if isinstance(response.data, list) and response.data:
            return response.data[0].get("existe", False)
        return False
    except Exception:
        return False

def verificar_formulario_comision(supabase: Client, cuil: str, comision_id: str) -> bool:
    try:
        response = supabase.rpc("verificar_formulario_comision", {
            "cuil_input": cuil,
            "comision_id_input": comision_id
        }).execute()
        if isinstance(response.data, list) and response.data:
            return response.data[0].get("existe", False)
        return False
    except Exception:
        return False

def obtener_datos_para_formulario(supabase: Client, cuil: str) -> dict:
    try:
        response = supabase.rpc("obtener_datos_para_formulario", {"cuil_input": cuil}).execute()
        if response.data and isinstance(response.data, list):
            return response.data[0]  # Devuelve un dict
        return {}
    except Exception as e:
        st.error(f"Error al obtener los datos del formulario: {e}")
        return {}

def verificar_preinscripcion(supabase: Client, cuil: str, id_actividad: str, comision_id: str) -> dict:
    """
    Llama a la función RPC 'verificar_preinscripcion' en Supabase.
    Devuelve un dict con las banderas:
      - existe_agente
      - ya_aprobo
      - ya_inscripto
    """
    try:
        resp = supabase.rpc(
            "verificar_preinscripcion",
            {
                "cuil_input": cuil,
                "id_actividad_input": id_actividad,
                "comision_id_input": comision_id
            }
        ).execute()
        return resp.data[0] if resp.data else {}
    except Exception as e:
        st.error("❌ Error al verificar preinscripción en la base de datos.")
        st.exception(e)
        return {}



# ============================
# Tablas y vistas
# ============================
def obtener_comisiones_abiertas(supabase: Client):
    """
    Devuelve las comisiones abiertas desde la vista 'vista_comisiones_abiertas'
    """
    resp = supabase.table("vista_comisiones_abiertas").select("*").execute()
    return resp.data if resp.data else []

def obtener_inscripciones(supabase: Client):
    """
    Devuelve todas las inscripciones (tabla cursos_inscripciones)
    """
    resp = supabase.table("cursos_inscripciones").select("*").execute()
    return resp.data if resp.data else []

#def insertar_inscripcion(supabase: Client, datos: dict):
#    """
#    Inserta una inscripción en la tabla definitiva
#    """
#    resp = supabase.table("cursos_inscripciones_tmp").insert(datos).execute()
#    return resp

def insertar_inscripcion(supabase: Client, datos: dict):
    # ===========================
    # Debug inicial
    # ===========================
    st.write("🔧 DEBUG - Datos originales completos:", datos)

    payload = {
        "p_comision_id": str(datos["comision_id"]),
        "p_cuil": str(datos["cuil"]),
        "p_fecha_inscripcion": datos.get("fecha_inscripcion"),
        "p_estado_inscripcion": datos.get("estado_inscripcion", "Nueva"),
        "p_vacante": datos.get("vacante", False),
        "p_sexo": datos.get("sexo"),
        "p_situacion_revista": datos.get("situacion_revista"),
        "p_nivel": datos.get("nivel"),
        "p_grado": datos.get("grado"),
        "p_agrupamiento": datos.get("agrupamiento"),
        "p_tramo": datos.get("tramo"),
        "p_id_dependencia_simple": datos.get("id_dependencia_simple"),
        "p_id_dependencia_general": datos.get("id_dependencia_general"),
        "p_email": datos.get("email"),
        "p_email_alternativo": datos.get("email_alternativo"),
        "p_nivel_educativo": datos.get("nivel_educativo"),
        "p_titulo": datos.get("titulo"),
        "p_tareas_desarrolladas": datos.get("tareas_desarrolladas"),
        "p_fecha_nacimiento": datos.get("fecha_nacimiento"),
        "p_edad_inscripcion": datos.get("edad_inscripcion"),
    }

    # Debug del payload y tipos
    st.write("🔧 DEBUG - Payload:", payload)
    st.write("🔧 DEBUG - Tipos de datos:", {k: type(v).__name__ for k, v in payload.items()})

    # ===========================
    # Inserción directa (esperado que falle con RLS)
    # ===========================
    try:
        st.write("🔧 Intentando inserción directa...")
        direct_result = supabase.table("cursos_inscripciones").insert({
            "comision_id": datos["comision_id"],
            "cuil": str(datos["cuil"]),
            "fecha_inscripcion": datos.get("fecha_inscripcion"),
            "estado_inscripcion": datos.get("estado_inscripcion", "Nueva"),
            "vacante": datos.get("vacante", False),
            "sexo": datos.get("sexo"),
            "situacion_revista": datos.get("situacion_revista"),
            "nivel": datos.get("nivel"),
            "grado": datos.get("grado"),
            "agrupamiento": datos.get("agrupamiento"),
            "tramo": datos.get("tramo"),
            "id_dependencia_simple": datos.get("id_dependencia_simple"),
            "id_dependencia_general": datos.get("id_dependencia_general"),
            "email": datos.get("email"),
            "email_alternativo": datos.get("email_alternativo"),
            "nivel_educativo": datos.get("nivel_educativo"),
            "titulo": datos.get("titulo"),
            "tareas_desarrolladas": datos.get("tareas_desarrolladas"),
            "fecha_nacimiento": datos.get("fecha_nacimiento"),
            "edad_inscripcion": datos.get("edad_inscripcion"),
            "usuario": "form_anon",
            "fecha_modificado": "now()"
        }).execute()

        st.success("✅ Inserción directa exitosa")
        st.write("🔧 DEBUG - Respuesta inserción directa:", direct_result.data)
        return {"id": direct_result.data[0]["id"]}

    except Exception as direct_error:
        st.write(f"⚠️ Inserción directa falló (esperado con RLS): {direct_error}")

    # ===========================
    # Inserción vía RPC
    # ===========================
    try:
        st.write("🔧 Intentando con RPC...")
        resp = supabase.rpc("inscripciones_form_campus", payload).execute()
        st.write("🔧 DEBUG RPC Response:", resp)

        if resp.data:
            # Caso más común: lista con dicts [{"id": "..."}]
            if isinstance(resp.data, list) and isinstance(resp.data[0], dict) and "id" in resp.data[0]:
                return {"id": resp.data[0]["id"]}
            # Caso raro: lista de strings o un string directo
            elif isinstance(resp.data, str):
                return {"id": resp.data}
            elif isinstance(resp.data, list) and resp.data:
                return {"id": str(resp.data[0])}
            else:
                return {"id": str(resp.data)}

        # Si llegamos aquí, RPC se ejecutó pero no devolvió nada
        st.warning("⚠️ RPC ejecutado sin error pero sin data, verificando inserción...")
        check_result = supabase.table("cursos_inscripciones") \
            .select("id") \
            .eq("cuil", datos["cuil"]) \
            .eq("comision_id", datos["comision_id"]) \
            .order("fecha_modificado", desc=True) \
            .limit(1) \
            .execute()

        if check_result.data:
            st.success("✅ Verificación: El registro SÍ fue insertado")
            return {"id": check_result.data[0]["id"]}
        else:
            st.error("❌ Verificación: No se encontró el registro")
            return None

    except Exception as rpc_error:
        st.error(f"❌ Error en RPC: {str(rpc_error)}")
        st.write("🔧 DEBUG RPC Error completo:", rpc_error)

        # Como última opción, verificar si igual se insertó
        try:
            check_result = supabase.table("cursos_inscripciones") \
                .select("id") \
                .eq("cuil", datos["cuil"]) \
                .eq("comision_id", datos["comision_id"]) \
                .order("fecha_modificado", desc=True) \
                .limit(1) \
                .execute()
            if check_result.data:
                st.warning("⚠️ El RPC dio error pero el registro SÍ se insertó")
                return {"id": check_result.data[0]["id"]}
        except:
            pass

        return None
