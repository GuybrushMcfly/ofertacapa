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

    # Preparar campos
    df_comisiones["fecha_desde"] = pd.to_datetime(df_comisiones["fecha_desde"])
    df_comisiones["fecha_hasta"] = pd.to_datetime(df_comisiones["fecha_hasta"])
    df_comisiones["duracion_dias"] = (df_comisiones["fecha_hasta"] - df_comisiones["fecha_desde"]).dt.days

    # Crear columna combinada
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # =======================
    # Filtros integrados
    # =======================
    st.markdown("### 🎯 Filtros")
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

    # Aplicar filtros
    df_filtrado = df_comisiones.copy()
    if organismo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["organismo"] == organismo_sel]
    if modalidad_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_cursada"] == modalidad_sel]
    df_filtrado = df_filtrado[df_filtrado["duracion_dias"] <= duracion_sel]

    if df_filtrado.empty:
        st.warning("⚠️ No hay comisiones que coincidan con los filtros seleccionados.")
        return

    # Columnas a mostrar (sin Tramo, con link_externo)
    columnas_finales = [
        "Actividad (Comisión)", "fecha_desde", "fecha_hasta", "fecha_cierre",
        "creditos", "modalidad_cursada", "link_externo"
    ]

    # Verificar columnas existentes
    faltantes = [col for col in columnas_finales if col not in df_filtrado.columns]
    if faltantes:
        st.error(f"❌ Columnas faltantes: {faltantes}")
        st.stop()

    # Renombrar para visualización
    df_vista = df_filtrado[columnas_finales].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "link_externo": "Acciones"
    })

    # ========== TABLA HTML ==========
    def create_html_table(df):
        headers = ''.join(f"<th>{col}</th>" if col != "Acciones" else "<th>Acciones</th>" for col in df.columns)

        html = f"""
        <style>
        .courses-table {{
            width: 90%;
            margin: 0 auto;
            border-collapse: collapse;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            background-color: white;
        }}
        .courses-table thead tr {{
            background-color: #136ac1;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }}
        .courses-table th, .courses-table td {{
            padding: 10px 8px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .courses-table tbody tr {{
            background-color: #ffffff;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .courses-table tbody tr:hover {{
            background-color: #e3f2fd;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(19, 106, 193, 0.3);
        }}
        .courses-table a.boton {{
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
        .courses-table a.boton:hover {{
            background-color: #136ac1;
            color: white;
            transform: scale(1.05);
        }}
        .no-link {{
            color: #bdc3c7;
            font-style: italic;
        }}
        </style>

        <table class="courses-table">
            <thead>
                <tr>{headers}</tr>
            </thead>
            <tbody>
        """

        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                val = row[col]
                if col == "Acciones":
                    html += '<td style="display:flex; gap:6px; flex-wrap: wrap;">'
                    if pd.notna(val) and val and val != "None":
                        html += f'<a href="{val}" target="_blank" class="boton">🌐 Acceder</a>'
                    else:
                        html += '<span class="no-link">Sin enlace</span>'
                    html += f'<a href="/preinscripcion" class="boton">📝 INDEC</a></td>'
                else:
                    html += f"<td>{val}</td>"
            html += "</tr>"

        html += "</tbody></table>"
        return html

    # ========== ESTILOS Y RENDER ==========
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100% !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        iframe {
            width: 100% !important;
        }
        .element-container {
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render
    html_code = create_html_table(df_vista)
    altura = min(800, 100 + (len(df_vista) * 45))
    components.html(html_code, height=altura, scrolling=True)
