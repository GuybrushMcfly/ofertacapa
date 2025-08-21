import os
import streamlit as st
from supabase import create_client, Client

# ----------------------------
# Conexión a Supabase
# ----------------------------
@st.cache_resource
def get_supabase_client() -> Client:
    """
    Devuelve un cliente de Supabase cacheado en memoria
    """
    url = os.environ.get("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_ANON_KEY") or st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

# ----------------------------
# FUNCIONES RPC
# ----------------------------
def verificar_formulario_cuil(supabase: Client, cuil: str):
    """
    Verifica si un CUIL corresponde a un agente activo en la base
    """
    return supabase.rpc("verificar_formulario_cuil", {"cuil_input": cuil}).execute()

def verificar_formulario_historial(supabase: Client, cuil: str, actividad_id: str):
    """
    Verifica si el agente ya aprobó la actividad indicada
    """
    return supabase.rpc("verificar_formulario_historial", {
        "cuil_input": cuil,
        "actividad_input": actividad_id
    }).execute()

def verificar_formulario_inscripcion(supabase: Client, cuil: str, comision_id: str):
    """
    Verifica si el agente ya está inscripto en la comisión indicada
    """
    return supabase.rpc("verificar_formulario_inscripcion", {
        "cuil_input": cuil,
        "comision_input": comision_id
    }).execute()

def obtener_datos_para_formulario(supabase: Client, cuil: str):
    """
    Obtiene todos los datos del agente necesarios para preinscripción
    """
    return supabase.rpc("obtener_datos_para_formulario", {"cuil_input": cuil}).execute()
