# espacio-ofertas.py
import streamlit as st

st.set_page_config(page_title="Espacio de Ofertas de Capacitación", layout="wide")

# =========================
# Inicializar vista actual
# =========================
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "destacados"  # por defecto

# =========================
# Estilo CSS de tabs (como Evaluaciones)
# =========================
st.markdown("""
<style>
.tab-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
.tab-button {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    padding: 10px 20px;
    margin: 0 5px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    text-align: center;
}
.tab-button:hover {
    background-color: #e3f2fd;
    border-color: #136ac1;
}
.tab-active {
    background-color: #136ac1 !important;
    color: white !important;
    border: 1px solid #136ac1 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Tabs de navegación
# =========================
tabs = ["tutorial", "destacados", "ofertas", "preinscripcion"]
labels = ["📘 Tutorial", "🌟 Destacados", "📚 Ofertas", "📝 Preinscripción"]

cols = st.columns(len(tabs))

for i, (tab, label) in enumerate(zip(tabs, labels)):
    with cols[i]:
        # Si se hace clic, cambia la vista
        if st.button(label, key=f"btn_{tab}"):
            st.session_state.vista_actual = tab

        # Pintar activo o inactivo
        if st.session_state.vista_actual == tab:
            st.markdown(f"<div class='tab-button tab-active'>{label}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='tab-button'>{label}</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# Renderizar vistas
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
