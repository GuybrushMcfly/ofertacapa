# views/destacados.py
import streamlit as st
import pandas as pd
from modules.db import get_supabase_client, obtener_comisiones_abiertas

def mostrar():
    st.markdown("## 🌟 Actividades destacadas")

    supabase = get_supabase_client()
    df_comisiones = pd.DataFrame(obtener_comisiones_abiertas(supabase))

    if df_comisiones.empty or "oferta_destacada" not in df_comisiones.columns:
        st.info("ℹ️ Actualmente no hay actividades destacadas.")
        return

    # Filtrar solo las destacadas (hasta 6)
    destacados = df_comisiones[df_comisiones["oferta_destacada"] == True].head(6)

    if destacados.empty:
        st.info("ℹ️ Actualmente no hay actividades destacadas.")
        return

    destacados = destacados.to_dict(orient="records")

    # ===================== ESTILO TARJETAS =====================
    st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* siempre 3 columnas */
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 15px;
        border-left: 5px solid #136ac1;
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 200px; /* altura fija */
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
        margin-bottom: 6px;
        font-size: 15px;
    }
    .card p {
        color: #333;
        font-size: 13px;
        text-align: left;
        margin: 0;
    }
    .card a {
        background-color: #136ac1;
        color: white !important;
        text-decoration: none;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 12px;
        transition: background-color 0.2s ease;
        display: inline-block;
        text-align: center;
    }
    .card a:hover {
        background-color: #0d4a87;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===================== ARMAR HTML DE TARJETAS =====================
    html_tarjetas = "<div class='card-grid'>"

    for d in destacados:
        titulo = d.get("nombre_actividad", "Actividad")
        comision = d.get("id_comision_sai", "")
        modalidad = d.get("modalidad_cursada", "")
        creditos = d.get("creditos", "-")
        fecha_desde = d.get("fecha_desde", "")
        fecha_hasta = d.get("fecha_hasta", "")
        link = d.get("link_externo") or ""

        # Formatear fechas
        fechas = ""
        if fecha_desde and fecha_hasta:
            try:
                fecha_desde_fmt = pd.to_datetime(fecha_desde).strftime("%d/%m/%Y")
                fecha_hasta_fmt = pd.to_datetime(fecha_hasta).strftime("%d/%m/%Y")
                fechas = f"{fecha_desde_fmt} al {fecha_hasta_fmt}"
            except:
                pass

        boton = f'<a href="{link}" target="_blank">🌐 Acceder</a>' if link else '<span style="color:#999;font-size:12px;">Sin enlace</span>'

        html_tarjetas += f"""
        <div class="card">
            <div>
                <h4>{titulo} ({comision})</h4>
                <p>
                    📅 {fechas if fechas else ''}<br>
                    🎓 {modalidad if modalidad else ''}<br>
                    ⭐ Créditos: {creditos if creditos not in [None, "nan", "NaN"] else "-"}
                </p>
            </div>
            <div>{boton}</div>
        </div>
        """

    html_tarjetas += "</div>"

    # Renderizar todas las tarjetas en bloque
    st.markdown(html_tarjetas, unsafe_allow_html=True)
