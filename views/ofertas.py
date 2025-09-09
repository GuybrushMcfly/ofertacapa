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
        filtro_org = st.selectbox("Filtrar por Organismo", organismos)
    with col2:
        filtro_mod = st.selectbox("Filtrar por Modalidad", modalidades)
    with col3:
        filtro_dur = st.selectbox("Filtrar por Duración", duraciones)

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
        "link_externo": "Link Externo"
    })

    # ✅ Mostrar mensaje visual si el DataFrame está vacío (como en el form.py original)
    if df_vista.empty:
        st.info("🔍 No hay cursos que coincidan con los filtros seleccionados.")
        return

    # ========== TABLA HTML ==========
  #font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
           #f   font-family: "Source Sans Pro", sans-serif;            

  
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

        /* Media query para móviles */
        @media screen and (max-width: 768px) {{
            .courses-table {{
                display: none !important;
            }}
            
            .mobile-cards {{
                display: block !important;
            }}
        }}

        @media screen and (min-width: 769px) {{
            .mobile-cards {{
                display: none !important;
            }}
        }}

        /* Estilos para las tarjetas móviles */
        .mobile-cards {{
            display: none;
        }}

        .mobile-card {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 12px;
            padding: 16px;
            border-left: 4px solid #136ac1;
        }}

        .card-title {{
            font-weight: bold;
            color: #136ac1;
            font-size: 14px;
            margin-bottom: 12px;
            line-height: 1.3;
        }}

        .card-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 12px;
        }}

        .card-info-item {{
            display: flex;
            flex-direction: column;
        }}

        .card-info-label {{
            font-weight: bold;
            color: #666;
            font-size: 11px;
        }}

        .card-info-value {{
            color: #333;
            margin-top: 2px;
        }}

        .card-link {{
            text-align: center;
            margin-top: 8px;
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
                if col == "Link Externo":
                    ...
                elif col in ["Inicio", "Fin", "Cierre"]:
                    if pd.notna(val) and val != "":
                        fecha_iso = pd.to_datetime(val, dayfirst=True, errors="coerce").strftime("%Y-%m-%d")
                        fecha_display = pd.to_datetime(val, dayfirst=True, errors="coerce").strftime("%d/%m/%Y")
                        html += f'<td data-order="{fecha_iso}">{fecha_display}</td>'
                    else:
                        html += "<td></td>"
                else:
                    html += f"<td>{val}</td>"
            html += "</tr>"


        html += """
            </tbody>
        </table>
        </div>
        
        <!-- Vista móvil con tarjetas -->
        <div class="mobile-cards" id="mobile-cards">
        """

        # Generar tarjetas móviles
        for _, row in df.iterrows():
            actividad = row["Actividad (Comisión)"]
            inicio = row["Inicio"]
            fin = row["Fin"]
            cierre = row["Cierre"]
            creditos = row["Créditos"]
            modalidad = row["Modalidad"]
            link = row["Link Externo"]

            html += f"""
            <div class="mobile-card">
                <div class="card-title">{actividad}</div>
                <div class="card-info">
                    <div class="card-info-item">
                        <span class="card-info-label">INICIO</span>
                        <span class="card-info-value">{inicio}</span>
                    </div>
                    <div class="card-info-item">
                        <span class="card-info-label">FIN</span>
                        <span class="card-info-value">{fin}</span>
                    </div>
                    <div class="card-info-item">
                        <span class="card-info-label">CIERRE</span>
                        <span class="card-info-value">{cierre}</span>
                    </div>
                    <div class="card-info-item">
                        <span class="card-info-label">CRÉDITOS</span>
                        <span class="card-info-value">{creditos}</span>
                    </div>
                </div>
                <div style="margin-bottom: 8px;">
                    <span class="card-info-label">MODALIDAD:</span> {modalidad}
                </div>
                <div class="card-link">
            """

            if pd.notna(link) and link and link != "None":
                html += f'<a href="{link}" target="_blank" class="boton">Form. INAP</a>'
            else:
                html += '<span class="no-link">Sin enlace</span>'

            html += """
                </div>
            </div>
            """

        html += "</div>  <!-- Cierre mobile-cards -->"

        # Script DataTables para paginación y ordenamiento
        html += """
        <script>
        $(document).ready(function() {
            $('#tabla-cursos').DataTable({
                paging: true,
                pageLength: 8,
                searching: false,
                info: false,
                lengthChange: false,
                fixedHeader: true,
                order: [], 
                columnDefs: [
                    { targets: 0, width: "40%" },  // Actividad
                    { targets: [1,2,3], type: "date", width: "10%" }, // Fechas ordenables
                    { targets: 4, width: "5%" },   // Créditos
                    { targets: 5, width: "10%" },  // Modalidad
                    { targets: 6, width: "20%" }   // Acciones
                ],
                language: {
                    paginate: { previous: "Anterior", next: "Siguiente" }
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
    altura_desktop = 180 + (filas_visibles * 45)   # Para tabla desktop
    altura_minima_movil = 600   # Altura mínima para que se vean bien las tarjetas móviles
    altura = max(altura_desktop, altura_minima_movil)
    
    components.html(html_code, height=altura, scrolling=True)
