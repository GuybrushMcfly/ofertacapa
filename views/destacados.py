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
        background-color: #f9f9f9;
        padding: 15px;
        border-left: 5px solid #136ac1;
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .destacada-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(19, 106, 193, 0.2);
    }
    
    .destacada-card h5 {
        color: #136ac1;
        margin-bottom: 8px;
        font-size: 14px;
        line-height: 1.2;
    }
    
    .destacada-card p {
        color: #333;
        font-size: 12px;
        margin-bottom: 8px;
        flex-grow: 1;
    }
    
    .card-button {
        background-color: #136ac1;
        color: white;
        text-decoration: none;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        transition: background-color 0.2s ease;
        display: inline-block;
        text-align: center;
        margin-top: 5px;
        border: none;
        cursor: pointer;
    }
    
    .card-button:hover {
        background-color: #0d4a87;
        color: white;
        text-decoration: none;
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
                
                # Crear la tarjeta con HTML
                card_content = f"""
                <div class="destacada-card">
                    <div>
                        <h5>{titulo} ({comision})</h5>
                        <p>{fechas}<br>{modalidad}{' · ' + str(creditos) + ' créditos' if creditos else ''}</p>
                    </div>
                </div>
                """
                
                st.markdown(card_content, unsafe_allow_html=True)
                
                # Botón de acceso (usando Streamlit nativo)
                if link:
                    st.markdown(f'<a href="{link}" target="_blank" style="background-color:#136ac1;color:white;text-decoration:none;padding:6px 10px;border-radius:4px;font-size:12px;display:inline-block;">🌐 Acceder</a>', unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#999;font-size:11px;">Sin enlace disponible</span>', unsafe_allow_html=True)
                    
            else:
                # Tarjeta vacía
                st.markdown("""
                <div class="destacada-empty">
                    Próximamente más actividades
                </div>
                """, unsafe_allow_html=True)
