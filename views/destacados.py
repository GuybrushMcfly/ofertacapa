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

    # Limitar a 6
    destacados = df_destacadas.head(6).to_dict(orient="records")

    # ===================== ESTILO TARJETAS =====================
    st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-top: 20px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-left: 5px solid #136ac1;
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    }
    .card h4 {
        color: #136ac1;
        margin-bottom: 10px;
    }
    .card p {
        color: #333;
        font-size: 14px;
        flex-grow: 1;
        text-align: justify;
    }
    .card a {
        background-color: #136ac1;
        color: white !important;
        text-decoration: none;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 13px;
        transition: background-color 0.2s ease;
        display: inline-block;
        text-align: center;
    }
    .card a:hover {
        background-color: #0d4a87;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===================== RENDER DE TARJETAS =====================
    # ===================== RENDER DE TARJETAS =====================
    cards_html = "<div class='card-grid'>"
    
    for d in destacados:
        titulo = d.get("nombre_actividad", "")
        comision = d.get("id_comision_sai", "")
        fechas = ""
        if d.get("fecha_desde") and d.get("fecha_hasta"):
            fechas = f"{pd.to_datetime(d['fecha_desde']).strftime('%d/%m/%Y')} al {pd.to_datetime(d['fecha_hasta']).strftime('%d/%m/%Y')}"
        modalidad = d.get("modalidad_cursada", "")
        creditos = d.get("creditos", "")
        link = d.get("link_externo", "")
    
        cards_html += f"""
        <div class="card">
            <div>
                <h4>{titulo} ({comision})</h4>
                <p>{fechas}<br>{modalidad}{' · ' + str(creditos) + ' créditos' if creditos else ''}</p>
            </div>
            <div>
                {'<a href="'+link+'" target="_blank">🌐 Acceder</a>' if link else '<span style="color:#999;font-size:12px;">Sin enlace</span>'}
            </div>
        </div>
        """
    
    cards_html += "</div>"
    
    # 🚀 Render final (interpreta HTML real, no texto plano)
    st.markdown(cards_html, unsafe_allow_html=True)

