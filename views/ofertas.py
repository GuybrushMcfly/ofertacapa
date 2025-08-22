import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
  #  st.header("📚 Ofertas de cursos")

    st.markdown(
        "<h4 style='text-align: center; color: #136ac1;'>📚 OFERTAS DISPONIBLES DE CAPACITACIONES</h3>",
        unsafe_allow_html=True
    )

    # Conexión a Supabase
    supabase = get_supabase_client()
    data = obtener_comisiones_abiertas(supabase)

    if not data:
        st.warning("No se encontraron cursos disponibles.")
        return

    # Convertir a DataFrame
    df_comisiones = pd.DataFrame(data)

    # Crear columna combinada: Actividad (Comisión)
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # Clasificar duración según créditos
    df_comisiones["creditos"] = df_comisiones["creditos"].fillna(0).astype(int)
    def clasificar_duracion(c):
        if c < 10: return "BREVE"
        elif c < 20: return "INTERMEDIA"
        else: return "PROLONGADA"
    df_comisiones["duracion"] = df_comisiones["creditos"].apply(clasificar_duracion)

    # Formatear fechas en formato dd-mm-yyyy
    for col in ["fecha_desde", "fecha_hasta", "fecha_cierre"]:
        df_comisiones[col] = pd.to_datetime(df_comisiones[col]).dt.strftime("%d-%m-%Y")

    # FILTROS: Organismo, Modalidad, Duración
    organismos = ["Todos"] + sorted(df_comisiones["organismo"].dropna().unique().tolist())
    modalidades = ["Todas"] + sorted(df_comisiones["modalidad_cursada"].dropna().unique().tolist())
    duraciones = ["Todas"] + sorted(df_comisiones["duracion"].unique())

    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_org = st.selectbox("Organismo", organismos)
    with col2:
        filtro_mod = st.selectbox("Modalidad", modalidades)
    with col3:
        filtro_dur = st.selectbox("Duración", duraciones)

    # Aplicar filtros según selección
    df_filtrado = df_comisiones.copy()
    if filtro_org != "Todos":
        df_filtrado = df_filtrado[df_filtrado["organismo"] == filtro_org]
    if filtro_mod != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_cursada"] == filtro_mod]
    if filtro_dur != "Todas":
        df_filtrado = df_filtrado[df_filtrado["duracion"] == filtro_dur]

    # Ordenar internamente por fecha_difusion (descendente)
    if "fecha_difusion" in df_filtrado.columns:
        df_filtrado = df_filtrado.assign(
            _fecha_difusion_orden=pd.to_datetime(df_filtrado["fecha_difusion"], dayfirst=True, errors="coerce")
        ).sort_values("_fecha_difusion_orden", ascending=False).drop(columns=["_fecha_difusion_orden"])



    # Columnas a mostrar en la tabla
    columnas_finales = [
        "Actividad (Comisión)", "fecha_desde", "fecha_hasta", "fecha_cierre",
        "creditos", "modalidad_cursada", "link_externo"
    ]
    faltantes = [col for col in columnas_finales if col not in df_filtrado.columns]
    if faltantes:
        st.error(f"❌ Columnas faltantes: {faltantes}")
        st.stop()

    # Renombrar columnas para visualización
    df_vista = df_filtrado[columnas_finales].rename(columns={
        "fecha_desde": "Inicio",
        "fecha_hasta": "Fin",
        "fecha_cierre": "Cierre",
        "creditos": "Créditos",
        "modalidad_cursada": "Modalidad",
        "link_externo": "Externo"
    })

    # ✅ Mostrar mensaje visual si el DataFrame está vacío (como en el form.py original)
    if df_vista.empty:
        st.info("🔍 No hay cursos que coincidan con los filtros seleccionados.")
        return

    # ========== TABLA HTML ==========
    def create_html_table(df):
        headers = ''.join(f"<th>{col}</th>" for col in df.columns)

        html = f"""
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
        <link rel="stylesheet" href="https://cdn.datatables.net/fixedheader/3.3.2/css/fixedHeader.dataTables.min.css">
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/fixedheader/3.3.2/js/dataTables.fixedHeader.min.js"></script>


        <style>
        .courses-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
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
        }}
        .courses-table tbody tr:hover {{
            background-color: #e3f2fd;
            transform: translateY(-1px);
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

        <div style="overflow-x:auto">
        <table class="courses-table" id="tabla-cursos">
            <thead>
                <tr>{headers}</tr>
            </thead>
            <tbody>
        """

        # Agregar filas
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                val = row[col]
                if col == "Externo":
                    html += '<td>'
                    if pd.notna(val) and val and val != "None":
                        
                        html += f'<a href="{val}" target="_blank" class="boton"> Form. INAP</a>'

                    else:
                        html += '<span class="no-link">Sin enlace</span>'
                    html += '</td>'
                else:
                    html += f"<td>{val}</td>"
            html += "</tr>"

        html += """
            </tbody>
        </table>
        </div>
        """

        # Script DataTables para paginación y ordenamiento
        html += """
        <script>
        $(document).ready(function() {
            $('#tabla-cursos').DataTable({
                paging: true,        // ✅ paginación siempre
                pageLength: 8,      // ✅ máximo 10 por página
                searching: false,
                info: false,
                lengthChange: false,
                fixedHeader: true,   // ✅ encabezado fijo
                order: [],
                columnDefs: [
                    { targets: 0, width: "40%" },  // Actividad (Comisión)
                    { targets: 1, width: "10%" },  // Inicio
                    { targets: 2, width: "10%" },  // Fin
                    { targets: 3, width: "10%" },  // Cierre
                    { targets: 4, width: "5%" },  // Créditos
                    { targets: 5, width: "10%" },  // Modalidad
                    { targets: 6, width: "20%" }   // Acciones
                ],
                language: {
                    paginate: {
                        previous: "Anterior",
                        next: "Siguiente"
                    }
                }
            });


        });
        </script>
        """
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


   
    # Render tabla final
    html_code = create_html_table(df_vista)
    
    # Altura dinámica: hasta 10 filas + espacio extra para paginación
    max_filas = 8
    filas_visibles = min(len(df_vista), max_filas)
    altura = 180 + (filas_visibles * 45)   # 140 en lugar de 100 para sumar espacio al footer
    
    components.html(html_code, height=altura, scrolling=False)




