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

    # Crear columna combinada
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # Columnas a mostrar (sin Tramo, y con link_externo)
    columnas_finales = [
        "Actividad (Comisión)", "fecha_desde", "fecha_hasta", "fecha_cierre",
        "creditos", "modalidad_cursada", "link_externo"
    ]

    # Verificar existencia de columnas antes de continuar
    faltantes = [col for col in columnas_finales if col not in df_comisiones.columns]
    if faltantes:
        st.error(f"❌ Columnas faltantes: {faltantes}")
        st.stop()

    df_vista = df_comisiones[columnas_finales].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "link_externo": "INAP"
    })

    # ========== TABLA HTML PERSONALIZADA ==========
    def create_html_table(df):
        html = """
        <style>
        .courses-table {
            width: 90%;
            margin: 0 auto;
            border-collapse: collapse;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            background-color: white;
        }
        .courses-table thead tr {
            background-color: #136ac1;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }
        .courses-table th, .courses-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        .courses-table tbody tr {
            background-color: #ffffff;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .courses-table tbody tr:hover {
            background-color: #e3f2fd;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(19, 106, 193, 0.3);
        }
        .courses-table a.boton {
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
        .courses-table a.boton:hover {
            background-color: #136ac1;
            color: white;
            transform: scale(1.05);
        }
        .no-link {
            color: #bdc3c7;
            font-style: italic;
        }
        </style>
        <table class="courses-table">
            <thead>
                <tr>
                    {headers}
                </tr>
            </thead>
            <tbody>
        """.format(headers=''.join(f"<th>{col}</th>" if col != "INAP" else "<th>Acciones</th>" for col in df.columns))

        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                val = row[col]
                if col == "INAP":
                    html += '<td style="display:flex; gap:6px; flex-wrap: wrap;">'
                    if pd.notna(val) and val:
                        html += f'<a href="{val}" target="_blank" class="boton">🌐 Acceder</a>'
                    else:
                        html += '<span class="no-link">Sin enlace</span>'
                    html += f'<a href="/preinscripcion" class="boton">📝 INDEC</a></td>'
                else:
                    html += f"<td>{val}</td>"
            html += "</tr>"

        html += "</tbody></table>"
        return html

    html_code = create_html_table(df_vista)

    # Ancho general y visual
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

    altura = min(800, 100 + (len(df_vista) * 45))
    components.html(html_code, height=altura, scrolling=True)
