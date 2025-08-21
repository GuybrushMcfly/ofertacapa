import streamlit as st
import pandas as pd
from modules.db import get_supabase_client, obtener_comisiones_abiertas
from modules.styles import css_tarjetas

def mostrar():
    st.header("🌟 Actividades destacadas")

    # Conexión a Supabase
    supabase = get_supabase_client()
    data = obtener_comisiones_abiertas(supabase)

    if not data:
        st.warning("No se encontraron actividades destacadas.")
        return

    # Convertir a DataFrame
    df_comisiones = pd.DataFrame(data)

    # Crear columna combinada (igual que en form.py)
    df_comisiones["Actividad (Comisión)"] = (
        df_comisiones["nombre_actividad"] + " (" + df_comisiones["id_comision_sai"] + ")"
    )

    # Tomar las primeras 6 como “destacadas”
    tarjetas = df_comisiones.head(6).to_dict(orient="records")

    # Ahora sí usamos el bloque de tarjetas (hover o con botones)
    css_tarjetas()
    st.subheader("🔹 Tarjetas con hover (zoom)")

    html_tarjetas = '<div class="card-grid">'
    for item in tarjetas:
        html_tarjetas += f"""
        <div class="card">
            <h4>{item['Actividad (Comisión)']}</h4>
            <p><b>📅 Fechas:</b> {item['fecha_desde']} al {item['fecha_hasta']}</p>
            <p><b>🎓 Modalidad:</b> {item['modalidad_cursada']}</p>
            <p><b>⭐ Créditos:</b> {item['creditos']}</p>
        </div>
        """
    html_tarjetas += '</div>'
    st.markdown(html_tarjetas, unsafe_allow_html=True)
