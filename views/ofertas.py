import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    st.header("📚 Ofertas de cursos")

    # =====================
    # Carga y preparación
    # =====================
    supabase = get_supabase_client()
    data = obtener_comisiones_abiertas(supabase)

    if not data:
        st.warning("No se encontraron cursos disponibles.")
        return

    df_comisiones = pd.DataFrame(data)

    # Convertimos fechas
    df_comisiones["fecha_desde"] = pd.to_datetime(df_comisiones["fecha_desde"])
    df_comisiones["fecha_hasta"] = pd.to_datetime(df_comisiones["fecha_hasta"])
    df_comisiones["duracion_dias"] = (df_comisiones["fecha_hasta"] - df_comisiones["fecha_desde"]).dt.days

    # Crear columna combinada
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # =====================
    # Filtros laterales
    # =====================
    st.sidebar.subheader("🎯 Filtros")

    organismos = sorted(df_comisiones["organismo"].dropna().unique())
    modalidades = sorted(df_comisiones["modalidad_cursada"].dropna().unique())

    organismo_sel = st.sidebar.selectbox("Organismo", ["Todos"] + organismos)
    modalidad_sel = st.sidebar.selectbox("Modalidad", ["Todas"] + modalidades)
    duracion_max = int(df_comisiones["duracion_dias"].max())
    duracion_sel = st.sidebar.slider("Duración máxima (días)", 1, duracion_max, duracion_max)

    df_filtrado = df_comisiones.copy()
    if organismo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["organismo"] == organismo_sel]
    if modalidad_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_cursada"] == modalidad_sel]
    df_filtrado = df_filtrado[df_filtrado["duracion_dias"] <= duracion_sel]

    if df_filtrado.empty:
        st.warning("⚠️ No hay comisiones que coincidan con los filtros seleccionados.")
        return

    # =====================
    # Preparación tabla
    # =====================
    columnas_finales = [
        "Actividad (Comisión)", "fecha_desde", "fecha_hasta", "fecha_cierre",
        "creditos", "modalidad_cursada", "link_externo"
    ]

    df_vista = df_filtrado[columnas_finales].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "link_externo": "Ver más"
    })

    # =====================
    # Formateo HTML + DataTables
    # =====================
    def formatear_link_html(url):
        if pd.isna(url) or url == "None":
            return '<span class="no-link">Sin enlace</span>'
        return f'<a href="{url}" target="_blank" class="boton">🌐 Acceder</a>'

    df_vista["Ver más"] = df_vista["Ver más"].apply(formatear_link_html)

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
        $('#ofertasTable').DataTable({
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

    <table id="ofertasTable" class="display" style="width:90%">
        <thead><tr>
    """

    for col in df_vista.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df_vista.iterrows():
        html += "<tr>"
        for col in df_vista.columns:
            if col == "Ver más":
                html += f"<td>{row[col]} <a href='/preinscripcion' class='boton'>📝 INDEC</a></td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"

    html += "</tbody></table>"

    altura = min(800, 100 + (len(df_vista) * 45))
    components.html(html, height=altura, scrolling=True)
