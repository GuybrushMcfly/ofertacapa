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
        st.warning("No se encontraron cursos con los filtros seleccionados.")
        return

    # Convertir a DataFrame
    df_comisiones = pd.DataFrame(data)

    # Recalcular columna combinada "Actividad (Comisión)"
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # Seleccionar columnas originales del formulario
    columnas_originales = [
        "Actividad (Comisión)",
        "fecha_desde",
        "fecha_hasta",
        "fecha_cierre",
        "creditos",
        "modalidad_cursada",
        "apto_tramo",
        "url_inap"
    ]

    columnas_existentes = [col for col in columnas_originales if col in df_comisiones.columns]

    df_vista = df_comisiones[columnas_existentes].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "apto_tramo": "Tramo",
        "url_inap": "INAP"
    })

    # =========================
    # Render tabla HTML con DataTables
    # =========================
    def create_html_table(df):
        table_id = "coursesTable"

        html = f"""
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>

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
        .courses-table a {{
            color: #136ac1;
            text-decoration: none;
            font-weight: bold;
            padding: 4px 8px;
            border: 2px solid #136ac1;
            border-radius: 5px;
            transition: all 0.3s ease;
            display: inline-block;
        }}
        .courses-table a:hover {{
            background-color: #136ac1;
            color: white;
            transform: scale(1.05);
        }}
        .no-link {{
            color: #bdc3c7;
            font-style: italic;
        }}
        </style>

        <table id="{table_id}" class="courses-table">
        <thead>
        <tr>
            {''.join(f'<th>{col}</th>' for col in df.columns)}
        </tr>
        </thead>
        <tbody>
        """

        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                val = row[col]
                if col == "INAP":
                    if pd.notna(val) and val:
                        html += f'<td><a href="{val}" target="_blank">🌐 Acceder</a></td>'
                    else:
                        html += '<td><span class="no-link">Sin enlace</span></td>'
                else:
                    html += f"<td>{val}</td>"
            html += "</tr>"

        html += f"""
        </tbody>
        </table>

        <script>
        $(document).ready(function() {{
            $('#{table_id}').DataTable({{
                pageLength: 10,
                dom: '<"top"f<"length-menu"l>>rt<"bottom"ip><"clear">',
                language: {{
                    search: "", searchPlaceholder: "🔍 Buscar...",
                    lengthMenu: "Mostrar _MENU_ registros por página",
                    zeroRecords: "No se encontraron resultados",
                    info: "Mostrando página _PAGE_ de _PAGES_",
                    infoEmpty: "No hay registros disponibles",
                    infoFiltered: "(filtrado de _MAX_ registros totales)",
                    paginate: {{ previous: "Anterior", next: "Siguiente" }}
                }}
            }});
            $(".dataTables_filter").css({{ "float": "left", "margin-bottom": "10px" }});
            $(".dataTables_filter input").css({{ "width": "300px" }});
            $(".dataTables_length").css({{ "float": "right" }});
        }});
        </script>
        """
        return html

    # Ajustar altura del iframe según cantidad de filas
    altura = min(800, 100 + (len(df_vista) * 45))

    # CSS para que no se “encajone”
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100% !important;
        padding: 0rem 2rem;
    }
    iframe {
        width: 100% !important;
        display: block;
    }
    .element-container {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render
    html_code = create_html_table(df_vista)
    components.html(html_code, height=altura, scrolling=True)
