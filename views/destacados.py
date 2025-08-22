# views/destacados.py
import streamlit as st
import pandas as pd
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    st.markdown("## 🌟 Actividades destacadas")
    
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
    
    # Primera fila (3 columnas)
    col1, col2, col3 = st.columns(3)
    columns_row1 = [col1, col2, col3]
    
    # Segunda fila (3 columnas)
    col4, col5, col6 = st.columns(3)
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
        
        st.info(f"📊 Mostrando ofertas {st.session_state.rotation_offset + 1} a {min(st.session_state.rotation_offset + 6, len(df_destacadas))} de {len(df_destacadas)} disponibles")
    
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
        font-size: 15px;
        font-weight: 700;
        line-height: 1.3;
        text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .card-dates {
        color: #2c5aa0;
        font-size: 12px;
        font-weight: 600;
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
        font-size: 11px;
        font-weight: 500;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    .card-credits {
        background: linear-gradient(90deg, #e8f2ff, #f0f8ff);
        color: #136ac1;
        font-size: 11px;
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
        background-color: #f5f5f5;
        border: 2px dashed #ddd;
        border-radius: 10px;
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        font-style: italic;
        font-size: 12px;
        margin-bottom: 10px;
        transition: transform 0.3s ease;
    }
    
    .destacada-empty:hover {
        transform: scale(1.02);
        border-color: #bbb;
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
                
                # Crear la tarjeta con HTML incluyendo el botón
                card_content = f"""
                <div class="destacada-card">
                    <div>
                        <h5>{titulo} ({comision})</h5>
                        <p>{fechas}<br>{modalidad}{' · ' + str(creditos) + ' créditos' if creditos else ''}</p>
                    </div>
                    <div>
                        {'<a href="'+link+'" target="_blank" class="card-button">🌐 Acceder</a>' if link else '<span style="color:#999;font-size:11px;">Sin enlace disponible</span>'}
                    </div>
                </div>
                """
                
                st.markdown(card_content, unsafe_allow_html=True)
                    
            else:
                # Tarjeta vacía
                st.markdown("""
                <div class="destacada-empty">
                    Próximamente más actividades
                </div>
                """, unsafe_allow_html=True)
