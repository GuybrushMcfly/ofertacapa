import streamlit as st

# ----------------------------
# CSS global para toda la app
# ----------------------------
def css_global():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton>button {
        background-color: #136ac1;
        color: white;
        border-radius: 6px;
        padding: 6px 12px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0f4f91;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# CSS de tablas de cursos
# ----------------------------
def css_tabla():
    st.markdown("""
    <style>
    .courses-table {
        width: 90%;
        margin: 0 auto;
        border-collapse: collapse;
        font-size: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden;
        background-color: white;
    }
    .courses-table thead tr {
        background-color: #136ac1;
        color: #ffffff;
        text-align: left;
        font-weight: bold;
    }
    .courses-table th, .courses-table td {
        padding: 10px 8px;
        border-bottom: 1px solid #e0e0e0;
    }
    .courses-table tbody tr {
        background-color: #ffffff;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .courses-table tbody tr:hover {
        background-color: #e3f2fd;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(19, 106, 193, 0.3);
    }
    .courses-table tbody tr.selected {
        background-color: #bbdefb !important;
        border-left: 4px solid #136ac1;
    }
    .courses-table a {
        color: #136ac1;
        text-decoration: none;
        font-weight: bold;
        padding: 4px 8px;
        border: 2px solid #136ac1;
        border-radius: 5px;
        transition: all 0.3s ease;
        display: inline-block;
    }
    .courses-table a:hover {
        background-color: #136ac1;
        color: white;
        transform: scale(1.05);
    }
    .no-link {
        color: #bdc3c7;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# CSS de tarjetas destacadas
# ----------------------------
def css_tarjetas():
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
        height: 220px;
    }
    .card:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    }
    .card h4 {
        margin-top: 0;
        font-size: 16px;
        color: #136ac1;
    }
    .card p {
        margin: 6px 0;
        font-size: 14px;
    }
    /* Responsivo */
    @media (max-width: 900px) {
      .card-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 600px) {
      .card-grid {
        grid-template-columns: 1fr;
      }
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# CSS animaciones flip (para tarjetas nuevas)
# ----------------------------
def css_flip_cards():
    st.markdown("""
    <style>
    .flip-card {
        background-color: transparent;
        width: 280px;
        height: 200px;
        perspective: 1000px;
        margin: 10px;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 15px;
    }
    .flip-card-front {
        background-color: #f9f9f9;
        color: #136ac1;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
    }
    .flip-card-back {
        background-color: #136ac1;
        color: white;
        transform: rotateY(180deg);
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)


# ----------------------------
# CSS para inputs de 1/3 pantalla
# ----------------------------
def css_inputs_un_tercio():
    st.markdown("""
    <style>
    input[type="text"] {
        width: 33% !important;   /* ocupa 1/3 del ancho */
        min-width: 300px;        /* evita que se achique demasiado */
    }
    </style>
    """, unsafe_allow_html=True)
