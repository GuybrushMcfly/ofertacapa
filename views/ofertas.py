import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.header("📚 Ofertas de cursos")

# Simulamos DataFrame de cursos
df = pd.DataFrame({
    "Actividad (Comisión)": ["Curso A (ABC123)", "Curso B (XYZ789)"],
    "Inicio": ["01-09-2025", "15-09-2025"],
    "Fin": ["10-09-2025", "20-09-2025"],
    "Modalidad": ["Virtual", "Presencial"]
})

# ========== TABLA HTML ========== #
def create_html_table(df):
    headers = ''.join(f"<th>{col}</th>" for col in df.columns)

    html = f"""
    <table border="1" style="border-collapse:collapse;width:100%">
        <thead><tr>{headers}<th>Acciones</th></tr></thead>
        <tbody>
    """
    for _, row in df.iterrows():
        actividad = row["Actividad (Comisión)"]
        html += "<tr>"
        for col in df.columns:
            html += f"<td>{row[col]}</td>"
        # 🚀 Botón Copiar que guarda en sessionStorage y fuerza rerun
        html += f"""
        <td>
            <a href="javascript:void(0);" 
               onclick="copyToField(`{actividad}`)" 
               style="color:#136ac1;font-weight:bold;">📋 Copiar</a>
        </td>
        """
        html += "</tr>"
    html += "</tbody></table>"

    # Script de copia
    html += """
    <script>
    function copyToField(value) {
        sessionStorage.setItem("campoLibre", value);
        window.parent.postMessage({type: "streamlit:rerun"}, "*");
    }
    </script>
    """
    return html

components.html(create_html_table(df), height=300, scrolling=True)

# ========== SCRIPT INVISIBLE PARA LEER sessionStorage ========== #
campo_code = """
<script>
const valor = sessionStorage.getItem("campoLibre") || "";
window.parent.postMessage({type: "setCampoLibre", value: valor}, "*");
</script>
"""
components.html(campo_code, height=0)

# Inicializar en session_state
if "campo_libre" not in st.session_state:
    st.session_state["campo_libre"] = ""

# Listener que engancha el valor enviado
message_code = """
<script>
window.addEventListener("message", (event) => {
    if (event.data.type === "setCampoLibre") {
        const input = window.parent.document.querySelector("input#campoLibreInput");
        if (input) {
            input.value = event.data.value;
            input.dispatchEvent(new Event("input", { bubbles: true }));
        }
    }
});
</script>
"""
components.html(message_code, height=0)

# Campo libre en Streamlit
st.session_state["campo_libre"] = st.text_input(
    "✍ Campo libre:",
    st.session_state["campo_libre"],
    key="campoLibreInput"
)

st.write("Valor actual:", st.session_state["campo_libre"])
