import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Espacio de Ofertas de Capacitación", layout="wide")

# Encabezado
st.markdown("<h1 style='font-size:26px;'>🎓 Espacio de Ofertas de Capacitación</h1>", unsafe_allow_html=True)

# ✅ Menú de navegación estilo horizontal
seleccion = option_menu(
    menu_title=None,
    options=["📘 Tutorial", "🌟 Destacados", "📚 Ofertas", "📝 Preinscripción"],
    icons=["book", "star", "book-half", "pencil-square"],
    orientation="horizontal",  # <- 👈 CLAVE: horizontal
    default_index=1,  # Por defecto "Destacados"
    styles={
        "container": {
            "display": "flex",
            "justify-content": "center",
            "background-color": "#ffffff",
            "margin-bottom": "20px"
        },
        "nav-link": {
            "font-size": "16px",
            "font-weight": "bold",
            "color": "#333333",
            "padding": "10px 20px",
            "margin": "0px 6px",
            "border-radius": "8px",
            "background-color": "#e6ecf3",
        },
        "nav-link-selected": {
            "background-color": "#2C75B2",
            "color": "#ffffff",
        },
    }
)

# =========================
# Renderizar vistas
# =========================
if seleccion == "📘 Tutorial":
    from views import tutorial
    tutorial.mostrar()

elif seleccion == "🌟 Destacados":
    from views import destacados
    destacados.mostrar()

elif seleccion == "📚 Ofertas":
    from views import ofertas
    ofertas.mostrar()

elif seleccion == "📝 Preinscripción":
    from views import preinscripcion
    preinscripcion.mostrar()
