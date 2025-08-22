# espacio-ofertas.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Espacio de Ofertas de Capacitación", layout="wide")

# ✅ 1. Capturar query param si llega desde botón HTML (ej: desde tabla)
if "selected_tab" in st.query_params:
    st.session_state.vista_actual = st.query_params["selected_tab"][0]
    st.query_params.clear()

# ✅ 2. Inicializar vista por defecto
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "destacados"

# ✅ 3. Estilos CSS personalizados (tipo option_menu)
st.markdown("""
<style>
.menu-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}
.menu-button {
    background-color: #C9D8E6;
    color: #1E1E1E;
    font-size: 17px;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    text-align: center;
    max-width: 280px;
    transition: background-color 0.3s ease;
}
.menu-button:hover {
    background-color: #B0C9E3;
}
.menu-button.active {
    background-color: #2C75B2;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ✅ 4. Botones de navegación HTML
tabs = ["tutorial", "destacados", "ofertas", "preinscripcion"]
labels = ["📘 Tutorial", "🌟 Destacados", "📚 Ofertas", "📝 Preinscripción"]

# Renderizado de botones
st.markdown('<div class="menu-container">', unsafe_allow_html=True)
for tab, label in zip(tabs, labels):
    active_class = "active" if st.session_state.vista_actual == tab else ""
    st.markdown(f"""
        <button class="menu-button {active_class}" onclick="
            window.parent.postMessage({{
                type: 'streamlit:setQueryParams',
                queryParams: {{ 'selected_tab': '{tab}' }}
            }}, '*');
            setTimeout(() => window.location.reload(), 100);
        ">{label}</button>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# ✅ 5. Renderizar vista correspondiente
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
