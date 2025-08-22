# views/destacados.py
import streamlit as st
import pandas as pd

def mostrar(df_comisiones: pd.DataFrame):
    st.markdown("## 🌟 Actividades destacadas")

    # Filtrar solo las destacadas
    destacados = df_comisiones[df_comisiones["oferta_destacada"] == True].head(6)

    if destacados.empty:
        st.info("📭 No hay ofertas destacadas en este momento.")
        return

    # ====== ESTILOS (idénticos a versión 2) ======
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
        font-size: 16px;
    }
    .card p {
        color: #333;
        font-size: 14px;
        margin: 0 0 10px 0;
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

    # ====== RENDER ======
    st.markdown("<div class='card-grid'>", unsafe_allow_html=True)

    for _, d in destacados.iterrows():
        titulo = f"{d.get('nombre_actividad','')} ({d.get('id_comision_sai','')})"
        fecha_desde = pd.to_datetime(d.get("fecha_desde")).strftime("%d/%m/%Y") if pd.notna(d.get("fecha_desde")) else ""
        fecha_hasta = pd.to_datetime(d.get("fecha_hasta")).strftime("%d/%m/%Y") if pd.notna(d.get("fecha_hasta")) else ""
        modalidad = d.get("modalidad_cursada", "")
        creditos = d.get("creditos", "")
        link = d.get("link_externo", "")

        st.markdown(f"""
        <div class="card">
            <div>
                <h4>{titulo}</h4>
                <p>📅 {fecha_desde} al {fecha_hasta}</p>
                <p>🎓 {modalidad}</p>
                <p>⭐ Créditos: {creditos}</p>
            </div>
            <div>
                {'<a href="'+link+'" target="_blank">🌐 Acceder</a>' if link else '<span style="color:#999;font-size:12px;">Sin enlace</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
