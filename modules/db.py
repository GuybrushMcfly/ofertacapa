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

def insertar_inscripcion(supabase: Client, datos: dict):
    """
    Inserta una inscripción en la tabla definitiva
    """
    resp = supabase.table("cursos_inscripciones").insert(datos).execute()
    return resp
