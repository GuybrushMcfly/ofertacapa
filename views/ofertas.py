import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    st.header("📚 Ofertas de cursos")

    supabase = get_supabase_client()
    data = obtener_comisiones_abiertas(supabase)

    if not data:
        st.warning("No se encontraron cursos disponibles.")
        return

    df = pd.DataFrame(data)

    # Preparación de fechas y campos
    df["fecha_desde"] = pd.to_datetime(df["fecha_desde"])
    df["fecha_hasta"] = pd.to_datetime(df["fecha_hasta"])
    df["duracion_dias"] = (df["fecha_hasta"] - df["fecha_desde"]).dt.days
    df["Actividad (Comisión)"] = df["nombre_actividad"] + " (" + df["id_comision_sai"] + ")"

    # ================== FILTROS EN EL CUERPO ==================
    st.markdown("### 🎯 Filtros")
    col1, col2, col3 = st.columns(3)

    with col1:
        orgs = sorted(df["organismo"].dropna().unique())
        organismo_sel = st.selectbox("Organismo", ["Todos"] + orgs)

    with col2:
        mods = sorted(df["modalidad_cursada"].dropna().unique())
        modalidad_sel = st.selectbox("Modalidad", ["Todas"] + mods)

    with col3:
        duracion_max = int(df["duracion_dias"].max())
        duracion_sel = st.slider("Duración máxima (días)", 1, duracion_max, duracion_max)

    df_filtrado = df.copy()
    if organismo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["organismo"] == organismo_sel]
    if modalidad_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_cursada"] == modalidad_sel]
    df_filtrado = df_filtrado[df_filtrado["duracion_dias"] <= duracion_sel]

    if df_filtrado.empty:
        st.warning("⚠️ No hay comisiones que coincidan con los filtros seleccionados.")
        return

    # ================== FORMATEO DE TABLA ==================
    def formatear_boton_html(url):
        if pd.isna(url) or url == "None":
            return '<span class="no-link">Sin enlace</span>'
        return f'<a href="{url}" target="_blank" class="boton">🌐 Acceder</a>'

    columnas = [
        "Actividad (Comisión)", "fecha_desde", "fecha_hasta", "fecha_cierre",
        "creditos", "modalidad_cursada", "link_externo"
    ]

    df_tabla = df_filtrado[columnas].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "link_externo": "Acción"
    })

    df_tabla["Acción"] = df_tabla["Acción"].apply(formatear_boton_html)

    # ================== HTML + DATATABLE ==================
    html = """
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>

    <style>
    .dataTables_wrapper .dataTables_paginate .paginate_button {
        padding: 4px 8px;
        margin: 2px;
        border-radius: 4px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
    }
    .boton {
        color: #136ac1;
        text-decoration: none;
        font-weight: bold;
        padding: 4px 8px;
        border: 2px solid #136ac1;
        border-radius: 5px;
        transition: all 0.3s ease;
        display: inline-block;
        margin-right: 6px;
    }
    .boton:hover {
        background-color: #136ac1;
        color: white;
        transform: scale(1.05);
    }
    .no-link {
        color: #bdc3c7;
        font-style: italic;
    }
    </style>

    <script>
    $(document).ready(function() {
        $('#tablaCursos').DataTable({
            paging: true,
            searching: false,
            info: false,
            lengthChange: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                },
                zeroRecords: "No hay resultados disponibles."
            }
        });
    });
    </script>

    <table id="tablaCursos" class="display" style="width:90%">
        <thead><tr>
    """

    for col in df_tabla.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df_tabla.iterrows():
        html += "<tr>"
        for col in df_tabla.columns:
            if col == "Acción":
                html += f"<td>{row[col]} <a href='/preinscripcion' class='boton'>📝 INDEC</a></td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"

    html += "</tbody></table>"

    altura = min(800, 100 + (len(df_tabla) * 45))
    components.html(html, height=altura, scrolling=True)
