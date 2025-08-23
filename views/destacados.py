# views/destacados.py
import streamlit as st
import pandas as pd
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    # ============================
    # 1) Conectar a Supabase y traer comisiones
    # ============================
    supabase = get_supabase_client()
    df_comisiones = pd.DataFrame(obtener_comisiones_abiertas(supabase))
    
    # Filtrar solo las actividades destacadas
    df_destacadas = df_comisiones[df_comisiones["oferta_destacada"] == True]
    
    if df_destacadas.empty:
        st.info("⚠️ No hay actividades destacadas disponibles por el momento.")
        return
    
    # ============================
    # 2) Inicializar las 6 tarjetas visibles
    # ============================
    destacados = df_destacadas.head(6).to_dict(orient="records")
    while len(destacados) < 6:
        destacados.append(None)  # Relleno para completar la grilla
    
    # ============================
    # 3) Sistema de rotación
    # ============================
    if len(df_destacadas) > 6:
        if 'rotation_offset' not in st.session_state:
            st.session_state.rotation_offset = 0
        

        
        # Obtener el grupo rotado de 6 elementos
        rotated_destacadas = df_destacadas.iloc[st.session_state.rotation_offset:].head(6)
        if len(rotated_destacadas) < 6:
            # Si faltan, traer desde el inicio
            extra = df_destacadas.head(6 - len(rotated_destacadas))
            rotated_destacadas = pd.concat([rotated_destacadas, extra])
        
        destacados = rotated_destacadas.to_dict(orient="records")
    
    # ============================
    # 4) Definir grilla de 6 columnas (2 filas de 3)
    # ============================
    col1, col2, col3 = st.columns(3, gap="large")
    col4, col5, col6 = st.columns(3, gap="large")
    all_columns = [col1, col2, col3, col4, col5, col6]
    
    # ============================
    # 5) Estilos CSS con comentarios
    # ============================
    st.markdown("""
    <style>
    /* === Tarjeta principal === */
    .destacada-card {
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%); /* Fondo degradado suave */
        padding: 18px;                /* Espaciado interno */
        border-left: 5px solid #c756aa; /* Borde lateral en color principal */
        border-radius: 12px;          /* Bordes redondeados */
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); /* Sombra sutil */
        height: 260px;                /* Altura fija para uniformidad */
        display: flex;                /* Layout flexible */
        flex-direction: column;       /* Apilar elementos verticalmente */
        justify-content: space-between; /* Separar título/detalles del botón */
        margin-bottom: 15px;          /* Espacio inferior */
        transition: all 0.3s ease;    /* Animación suave al hover */
        position: relative;           /* Para animaciones internas */
        overflow: hidden;
    }

    /* === Efecto hover de la tarjeta === */
    .destacada-card:hover {
        transform: translateY(-10px) scale(1.03); /* Se eleva y agranda un poco más */
        box-shadow: 0 16px 32px rgba(199, 86, 170, 0.35); /* Sombra más fuerte */
        border-left-color: #db6fc0; /* Cambio de color en el borde lateral */
    }

    /* === Título del curso === */
    .card-title {
        color: #c756aa;       /* Color principal */
        margin-bottom: 14px;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.4;
    }

    /* === Organismo (aparece antes de la fecha) === */
    .card-org {
        color: #5a5d61;       /* Color secundario */
        font-size: 12px;
        margin-bottom: 6px;
        font-weight: 600;
    }

    /* === Fechas del curso === */
    .card-dates {
        color: #5a5d61;       /* Color secundario */
        font-size: 12px;
        margin-bottom: 6px;
    }

    /* === Créditos y modalidad === */
    .card-info {
        color: #5a5d61;       /* Color secundario */
        font-size: 12px;
        margin-bottom: 8px;
        line-height: 1.4;
    }

    /* === Botón de acceso === */
    .card-button {
        background: linear-gradient(135deg, #c756aa 0%, #db6fc0 100%); /* Fondo degradado en tonos principales */
        color: white !important;
        text-decoration: none !important;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        text-align: center;
        width: 100%;
        transition: all 0.2s ease;
    }
    .card-button:hover {
        transform: translateY(-3px);  /* Hover más notorio */
        box-shadow: 0 6px 12px rgba(199, 86, 170, 0.4);
    }

    /* === Aviso cuando no hay link === */
    .no-link {
        color: #999;
        font-size: 11px;
        font-style: italic;
        text-align: center;
        padding: 6px;
        background: #f5f5f5;
        border-radius: 6px;
        margin-top: 6px;
    }

    /* === Tarjeta vacía (placeholder) === */
    .destacada-empty {
        background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
        border: 2px dashed #ddd;
        border-radius: 12px;
        height: 260px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        font-style: italic;
        font-size: 12px;
        transition: all 0.3s ease;
    }
    .destacada-empty:hover {
        transform: translateY(-4px);  /* También se levanta un poco al hover */
        border-color: #bbb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ============================
    # 6) Render de las tarjetas
    # ============================
    for i, col in enumerate(all_columns):
        with col:
            if i < len(destacados) and destacados[i] is not None:
                d = destacados[i]
                titulo = d.get("nombre_actividad", "")
                comision = d.get("id_comision_sai", "")
                organismo = d.get("organismo", "")
                
                # Fechas formateadas
                fechas_formatted = ""
                if d.get("fecha_desde") and d.get("fecha_hasta"):
                    fecha_desde = pd.to_datetime(d['fecha_desde']).strftime('%d/%m/%Y')
                    fecha_hasta = pd.to_datetime(d['fecha_hasta']).strftime('%d/%m/%Y')
                    fechas_formatted = f"{fecha_desde} al {fecha_hasta}"
                
                modalidad = d.get("modalidad_cursada", "")
                creditos = d.get("creditos", "")
                
                # Línea créditos + modalidad
                creditos_line = []
                if creditos:
                    creditos_line.append(f"🎓 {creditos} créditos")
                if modalidad:
                    creditos_line.append(f"🖥️ {modalidad}")
                creditos_modalidad_line = " • ".join(creditos_line)
                
                link = d.get("link_externo", "")
                
                # HTML de la tarjeta
                card_content = f"""
                <div class="destacada-card">
                    <div>
                        <div class="card-title"><strong>{titulo} ({comision})</strong></div>
                        {'<div class="card-org">🏢 ' + organismo + '</div>' if organismo else ''}
                        {'<div class="card-dates">📅 ' + fechas_formatted + '</div>' if fechas_formatted else ''}
                        {'<div class="card-info">' + creditos_modalidad_line + '</div>' if creditos_modalidad_line else ''}
                    </div>
                    <div>
                        {'<a href="'+link+'" target="_blank" class="card-button">🌐 Acceder al curso</a>' if link else '<div class="no-link">⚠️ Sin enlace disponible</div>'}
                    </div>
                </div>
                """
                st.markdown(card_content, unsafe_allow_html=True)
            else:
                # Tarjeta vacía
                st.markdown("""
                <div class="destacada-empty">
                    ⭐ Próximamente más actividades destacadas
                </div>
                """, unsafe_allow_html=True)

        # Botón para rotar la vista
        if st.button("🔄 Ver más ofertas destacadas", key="rotate_offers"):
            st.session_state.rotation_offset = (st.session_state.rotation_offset + 6) % len(df_destacadas)
