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
def verificar_formulario_cuil(supabase: Client, cuil: str):
    return supabase.rpc("verificar_formulario_cuil", {"cuil_input": cuil}).execute()

def obtener_datos_para_formulario(supabase: Client, cuil: str):
    return supabase.rpc("obtener_datos_para_formulario", {"cuil_input": cuil}).execute()

def verificar_formulario_historial(supabase: Client, cuil: str, actividad_id: str):
    return supabase.rpc("verificar_formulario_historial",
                        {"cuil_input": cuil, "actividad_id": actividad_id}).execute()

def verificar_formulario_inscripcion(supabase: Client, cuil: str, comision_id: str):
    return supabase.rpc("verificar_formulario_inscripcion",
                        {"cuil_input": cuil, "comision_id": comision_id}).execute()

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
    Devuelve todas las inscripciones (tabla cursos_inscripciones o pruebainscripciones)
    """
    resp = supabase.table("cursos_inscripciones").select("*").execute()
    return resp.data if resp.data else []

def insertar_inscripcion(supabase: Client, datos: dict):
    """
    Inserta una inscripción en la tabla definitiva
    """
    resp = supabase.table("cursos_inscripciones").insert(datos).execute()
    return resp
