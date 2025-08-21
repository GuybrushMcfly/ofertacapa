# espacio-ofertas.py
import streamlit as st

st.set_page_config(page_title="Preinscripción INAP", layout="wide")

# =========================
# Estado de navegación
# =========================
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "tutorial"

# =========================
# Botones de navegación
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📖 TUTORIAL"):
        st.session_state.vista_actual = "tutorial"

with col2:
    if st.button("🌟 DESTACADOS"):
        st.session_state.vista_actual = "destacados"

with col3:
    if st.button("📚 OFERTAS DE CURSOS"):
        st.session_state.vista_actual = "ofertas"

with col4:
    if st.button("📝 PREINSCRIPCIÓN"):
        st.session_state.vista_actual = "preinscripcion"

st.markdown("---")

# =========================
# Renderizado de cada vista
# =========================
if st.session_state.vista_actual == "tutorial":
    from views import tutorial
    tutorial.mostrar()

elif st.session_state.vista_actual == "destacados":
    from views import destacados
    destacados.mostrar()

elif st.session_state.vista_actual == "ofertas":
    from views import ofertas
    ofertas.mostrar()

elif st.session_state.vista_actual == "preinscripcion":
    from views import preinscripcion
    preinscripcion.mostrar()

