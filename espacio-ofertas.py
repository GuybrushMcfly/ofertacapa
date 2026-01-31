import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="🎓 Espacio de Ofertas de Capacitación", layout="wide")


st.markdown(
    """
    <style>
    /* Ocultar íconos de ancla en todos los títulos de Streamlit */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# Encabezado
# =========================
#st.markdown("<h1 style='font-size:26px;'>🎓 Espacio de Ofertas de Capacitación</h1>", unsafe_allow_html=True)

# =========================
# Navegación con botones horizontales (estilo Evaluaciones)
# =========================
seleccion = option_menu(
    menu_title=None,
    options=["❓ Preguntas", "🌟 Destacados", "📚 Listado Ofertas", "📝 Formulario INDEC"],
    orientation="horizontal",  # Botones horizontales
    default_index=1,  # Por defecto muestra 'Destacados'
    styles={
        "container": {
            "padding": "0!important", 
            "background-color": "transparent",
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0 10px",
            "max-width": "250px",
            "color": "1E1E1E",
            "font-weight": "bold",
            "background-color": "#C9D8E6",
            "border-radius": "8px",
            "--hover-color": "#B0C9E3",
        },
        "nav-link-selected": {
            "background-color": "#c756aa",
            "color": "#ffffff",
            "font-weight": "bold",
            "border-radius": "8px",
        },
    }
)

# =========================
# Renderizar vistas según selección
# =========================
if seleccion == "❓ Preguntas":
    from views import tutorial
    tutorial.mostrar()

elif seleccion == "🌟 Destacados":
    from views import destacados
    destacados.mostrar()

elif seleccion == "📚 Listado Ofertas":
    from views import ofertas
    ofertas.mostrar()

elif seleccion == "📝 Formulario INDEC":
    from views import preinscripcion
    preinscripcion.mostrar()
