import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    st.header("📚 Ofertas de cursos")

    # Conexión a Supabase
    supabase = get_supabase_client()
    data = obtener_comisiones_abiertas(supabase)

    if not data:
        st.warning("No se encontraron cursos disponibles.")
        return

    # Convertir a DataFrame
    df_comisiones = pd.DataFrame(data)

    # Calcular duración
    df_comisiones["fecha_desde"] = pd.to_datetime(df_comisiones["fecha_desde"])
    df_comisiones["fecha_hasta"] = pd.to_datetime(df_comisiones["fecha_hasta"])
    df_comisiones["duracion_dias"] = (df_comisiones["fecha_hasta"] - df_comisiones["fecha_desde"]).dt.days

    # Crear columna combinada
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # ========== FILTROS ==========
    col1, col2, col3 = st.columns(3)

    with col1:
        organismos = sorted(df_comisiones["organismo"].dropna().unique())
        organismo_sel = st.selectbox("Organismo", ["Todos"] + organismos)

    with col2:
        modalidades = sorted(df_comisiones["modalidad_cursada"].dropna().unique())
        modalidad_sel = st.selectbox("Modalidad", ["Todas"] + modalidades)

    with col3:
        duracion_max = int(df_comisiones["duracion_dias"].max())
        duracion_sel = st.slider("Duración máxima (días)", 1, duracion_max, duracion_max)

    df_filtrado = df_comisiones.copy()
    if organismo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["organismo"] == organismo_sel]
    if modalidad_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_cursada"] == modalidad_sel]
    df_filtrado = df_filtrado[df_filtrado["duracion_dias"] <= duracion_sel]

    if df_filtrado.empty:
        st.warning("⚠️ No hay comisiones que coincidan con los filtros seleccionados.")
        return

    # Columnas a mostrar (sin Tramo)
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

    # ========== TABLA HTML + JS ==========

    def formatear_link_html(url):
        if pd.isna(url) or url == "None":
            return '<span class="no-link">Sin enlace</span>'
        return f'<a href="{url}" target="_blank" class="boton">🌐 Acceder</a>'

    df_vista["Ver más"] = df_vista["Ver más"].apply(formatear_link_html)

    html = f"""
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>

    <style>
    .dataframe-container {{
        width: 90%;
        margin: 0 auto;
    }}
    table.dataTable thead {{
        background-color: #136ac1;
        color: white;
        font-weight: bold;
    }}
    .boton {{
        color: #136ac1;
        text-decoration: none;
        font-weight: bold;
        padding: 4px 8px;
        border: 2px solid #136ac1;
        border-radius: 5px;
        transition: all 0.3s ease;
        display: inline-block;
        margin-right: 6px;
    }}
    .boton:hover {{
        background-color: #136ac1;
        color: white;
        transform: scale(1.05);
    }}
    .no-link {{
        color: #bdc3c7;
        font-style: italic;
    }}
    </style>

    <div class="dataframe-container">
    <table id="tablaCursos" class="display">
        <thead>
            <tr>
                {''.join(f"<th>{col}</th>" for col in df_vista.columns[:-1])}
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
    """

    for _, row in df_vista.iterrows():
        html += "<tr>"
        for col in df_vista.columns[:-1]:
            html += f"<td>{row[col]}</td>"
        html += f"<td>{row['Ver más']}<a href='/preinscripcion' class='boton'>📝 INDEC</a></td>"
        html += "</tr>"

    html += """
        </tbody>
    </table>
    </div>

    <script>
    $(document).ready(function() {{
        $('#tablaCursos').DataTable({{
            paging: true,
            searching: false,
            language: {{
                "paginate": {{
                    "previous": "Anterior",
                    "next": "Siguiente"
                }},
                "info": "Mostrando _START_ a _END_ de _TOTAL_ cursos",
                "infoEmpty": "Sin cursos para mostrar",
                "emptyTable": "No hay datos disponibles"
            }}
        }});
    }});
    </script>
    """

    components.html(html, height=600, scrolling=True)
