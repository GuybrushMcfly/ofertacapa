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

    # Filtrar solo las destacadas
    destacados = df_comisiones[df_comisiones["oferta_destacada"] == True].head(6)

    # Si hay menos de 6 → rellenamos con tarjetas vacías
    if len(destacados) < 6:
        faltan = 6 - len(destacados)
        vacias = pd.DataFrame([{} for _ in range(faltan)])
        destacados = pd.concat([destacados, vacias], ignore_index=True)

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
        height: 200px; /* altura fija más compacta */
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
    .card-empty {
        background-color: #f0f0f0;
        border: 2px dashed #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===================== RENDER TARJETAS =====================
    st.markdown("<div class='card-grid'>", unsafe_allow_html=True)

    for d in destacados:
        if not d or "nombre_actividad" not in d:
            st.markdown("<div class='card card-empty'>Sin actividad destacada</div>", unsafe_allow_html=True)
            continue

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

        st.markdown(f"""
        <div class="card">
            <div>
                <h4>{titulo} ({comision})</h4>
                <p>
                    📅 {fechas}<br>
                    🎓 {modalidad}<br>
                    ⭐ Créditos: {creditos}
                </p>
            </div>
            <div>{boton}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
