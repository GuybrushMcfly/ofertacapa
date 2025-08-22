import streamlit as st
import pandas as pd

def mostrar(df_comisiones: pd.DataFrame):
    st.markdown("## 🌟 Actividades destacadas")

    # ===================== FILTRO POR DESTACADAS =====================
    if "oferta_destacada" not in df_comisiones.columns:
        st.warning("⚠️ La tabla no tiene el campo 'oferta_destacada'.")
        return

    destacados_df = df_comisiones[df_comisiones["oferta_destacada"] == True]

    if destacados_df.empty:
        st.info("ℹ️ No hay ofertas destacadas en este momento.")
        return

    # Tomar hasta 6 destacadas aleatorias (rotación)
    destacados = destacados_df.sample(n=min(6, len(destacados_df))).to_dict(orient="records")

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
    st.markdown("<div class='card-grid'>", unsafe_allow_html=True)

    for d in destacados:
        titulo = d.get("nombre_actividad", "Actividad")
        organismo = d.get("organismo", "Organismo")
        modalidad = d.get("modalidad_cursada", "")
        link = d.get("link_externo", "")

        st.markdown(f"""
        <div class="card">
            <div>
                <h4>{titulo}</h4>
                <p><b>{organismo}</b><br>{modalidad}</p>
            </div>
            <div>
                {'<a href="'+link+'" target="_blank">🌐 Acceder</a>' if link else '<span style="color:#999;font-size:12px;">Sin enlace</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
