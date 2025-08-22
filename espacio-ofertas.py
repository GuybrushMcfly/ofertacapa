# espacio-ofertas.py
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Espacio de Ofertas de Capacitación", layout="wide")

# =========================
# Estilo y navegación
# =========================
st.markdown("<h1 style='font-size:26px;'>🎓 Espacio de Ofertas de Capacitación</h1>", unsafe_allow_html=True)

# ✅ Botones tipo menú
seleccion = option_menu(
    menu_title=None,
    options=["📘 Tutorial", "🌟 Destacados", "📚 Ofertas", "📝 Preinscripción"],
    icons=["book", "star", "book-half", "pencil-square"],
    orientation="vertical",  # podés cambiarlo a "horizontal" si querés
    default_index=1,  # por defecto "Destacados"
    styles={
        "container": {
            "padding": "0!important", 
            "background-color": "transparent",
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "left",
            "margin": "6px 2px",
            "color": "#333333",
            "font-weight": "bold",
            "background-color": "#e6ecf3",
            "border-radius": "8px",
        },
        "nav-link-selected": {
            "background-color": "#2C75B2",
            "color": "#ffffff",
            "font-weight": "bold",
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
