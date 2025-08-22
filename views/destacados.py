# views/destacados.py
import streamlit as st
import pandas as pd
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
#    st.markdown("## 🌟 Actividades destacadas")
    
    # Conectar a Supabase
    supabase = get_supabase_client()
    df_comisiones = pd.DataFrame(obtener_comisiones_abiertas(supabase))
    
    # Filtrar destacadas
    df_destacadas = df_comisiones[df_comisiones["oferta_destacada"] == True]
    
    if df_destacadas.empty:
        st.info("⚠️ No hay actividades destacadas disponibles por el momento.")
        return
    
    # Limitar a 6 y asegurar que siempre tengamos 6 elementos (rellenando con vacíos)
    destacados = df_destacadas.head(6).to_dict(orient="records")
    
    # Rellenar hasta 6 elementos para mantener la grid completa
    while len(destacados) < 6:
        destacados.append(None)
    

    
    # ===================== RENDER DE TARJETAS =====================
    # Crear grid usando columnas de Streamlit (más confiable)
    
    # Primera fila (3 columnas con más separación)
    col1, col2, col3 = st.columns(3, gap="large")
    columns_row1 = [col1, col2, col3]
    
    # Segunda fila (3 columnas con más separación)
    col4, col5, col6 = st.columns(3, gap="large")
    columns_row2 = [col4, col5, col6]
    
    all_columns = columns_row1 + columns_row2
    
    # Sistema de rotación si hay más de 6 actividades destacadas
    if len(df_destacadas) > 6:
        # Usar session_state para manejar la rotación
        if 'rotation_offset' not in st.session_state:
            st.session_state.rotation_offset = 0
        
        # Botón para rotar las ofertas
        if st.button("🔄 Ver más ofertas destacadas", key="rotate_offers"):
            st.session_state.rotation_offset = (st.session_state.rotation_offset + 6) % len(df_destacadas)
        
        # Aplicar offset de rotación
        rotated_destacadas = df_destacadas.iloc[st.session_state.rotation_offset:].head(6)
        if len(rotated_destacadas) < 6:
            # Si no hay suficientes desde el offset, tomar del principio
            remaining = 6 - len(rotated_destacadas)
            extra = df_destacadas.head(remaining)
            rotated_destacadas = pd.concat([rotated_destacadas, extra])
        
        destacados = rotated_destacadas.to_dict(orient="records")
        
        # Información de rotación más discreta (opcional, se puede comentar/descomentar)
        # st.info(f"📊 Mostrando ofertas {st.session_state.rotation_offset + 1} a {min(st.session_state.rotation_offset + 6, len(df_destacadas))} de {len(df_destacadas)} disponibles")
    
    # Aplicar estilo para las tarjetas individuales con animaciones
    st.markdown("""
    <style>
    .destacada-card {
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        padding: 18px;
        border-left: 5px solid #136ac1;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .destacada-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #136ac1, #4fa8e8);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .destacada-card:hover::before {
        transform: scaleX(1);
    }
    
    .destacada-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 25px rgba(19, 106, 193, 0.15);
        border-left-color: #4fa8e8;
    }
    
    .card-title {
        color: #136ac1;
        margin-bottom: 12px;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.3;
        text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .card-dates {
        color: #2c5aa0;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
    }
    
    .card-dates::before {
        content: '📅';
        margin-right: 6px;
    }
    
    .card-info {
        color: #5a6c7d;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    .card-credits {
        background: linear-gradient(90deg, #e8f2ff, #f0f8ff);
        color: #136ac1;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #d1e7ff;
    }
    
    .card-button {
        background: linear-gradient(135deg, #136ac1 0%, #1e7fd4 100%);
        color: white !important;
        text-decoration: none !important;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
        display: inline-block;
        text-align: center;
        margin-top: 8px;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(19, 106, 193, 0.2);
        width: 100%;
    }
    
    .card-button:hover {
        background: linear-gradient(135deg, #0d4a87 0%, #1666b8 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(19, 106, 193, 0.3);
        color: white !important;
        text-decoration: none !important;
    }
    
    .no-link {
        color: #999;
        font-size: 11px;
        font-style: italic;
        text-align: center;
        padding: 8px;
        background: #f5f5f5;
        border-radius: 6px;
        margin-top: 8px;
    }
    
    .destacada-empty {
        background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
        border: 2px dashed #ddd;
        border-radius: 12px;
        height: 240px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #999;
        font-style: italic;
        font-size: 12px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .destacada-empty:hover {
        transform: translateY(-4px);
        border-color: #bbb;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    
    .destacada-empty::before {
        content: '⭐';
        font-size: 24px;
        margin-bottom: 8px;
        opacity: 0.5;
    }
    
    /* Animación de entrada suave */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .destacada-card, .destacada-empty {
        animation: fadeInUp 0.6s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Renderizar en cada columna
    for i, col in enumerate(all_columns):
        with col:
            if i < len(destacados) and destacados[i] is not None:
                d = destacados[i]
                titulo = d.get("nombre_actividad", "")
                comision = d.get("id_comision_sai", "")
                fechas = ""
                if d.get("fecha_desde") and d.get("fecha_hasta"):
                    fechas = f"{pd.to_datetime(d['fecha_desde']).strftime('%d/%m/%Y')} al {pd.to_datetime(d['fecha_hasta']).strftime('%d/%m/%Y')}"
                modalidad = d.get("modalidad_cursada", "")
                creditos = d.get("creditos", "")
                link = d.get("link_externo", "")
                
                # Procesar la información para mejor presentación
                fechas_formatted = ""
                if d.get("fecha_desde") and d.get("fecha_hasta"):
                    fecha_desde = pd.to_datetime(d['fecha_desde']).strftime('%d/%m/%Y')
                    fecha_hasta = pd.to_datetime(d['fecha_hasta']).strftime('%d/%m/%Y')
                    fechas_formatted = f"{fecha_desde} al {fecha_hasta}"
                
                modalidad_formatted = d.get("modalidad_cursada", "")
                creditos_text = ""
                if d.get("creditos"):
                    creditos_text = f"{creditos} créditos"
                
                # Crear línea de créditos + modalidad
                creditos_modalidad = []
                if creditos_text:
                    creditos_modalidad.append(f"🎓 {creditos_text}")
                if modalidad_formatted:
                    creditos_modalidad.append(f"🖥️ {modalidad_formatted}")
                creditos_modalidad_line = " • ".join(creditos_modalidad)
                
                # Crear la tarjeta con HTML mejorado
                card_content = f"""
                <div class="destacada-card">
                    <div style="flex-grow: 1;">
                        <div class="card-title"><strong>{titulo} ({comision})</strong></div>
                        {'<div class="card-dates">' + fechas_formatted + '</div>' if fechas_formatted else ''}
                        {'<div class="card-info">' + creditos_modalidad_line + '</div>' if creditos_modalidad_line else ''}
                    </div>
                    <div style="margin-top: auto;">
                        {'<a href="'+link+'" target="_blank" class="card-button">🌐 Acceder al curso</a>' if link else '<div class="no-link">⚠️ Sin enlace disponible</div>'}
                    </div>
                </div>
                """
                
                st.markdown(card_content, unsafe_allow_html=True)
                    
            else:
                # Tarjeta vacía con mejor diseño
                st.markdown("""
                <div class="destacada-empty">
                    <div style="text-align: center;">
                        <div style="font-size: 14px; font-weight: 600; margin-bottom: 4px;">Próximamente</div>
                        <div>Más actividades destacadas</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
