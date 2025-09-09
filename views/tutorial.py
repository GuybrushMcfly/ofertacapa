import streamlit as st

def mostrar():
    st.markdown(
        "<h4 style='text-align: center; color: #136ac1;'>⁉️ PREGUNTAS FRECUENTES</h3>",
        unsafe_allow_html=True
    )    

    # ===== CSS para tarjetas flip =====
    st.markdown("""
    <style>
    .flip-card {
      background-color: transparent;
      width: 350px;
      height: 200px;
      perspective: 1000px;
      margin: 10px auto;
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
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 12px;
      box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 15px;
    }
    .flip-card-front {
      background-color: #d14fbb;
      color: white;
      font-size: 18px;
      font-weight: bold;
    }
    .flip-card-back {
      background-color: #f9f9f9;
      color: #333;
      transform: rotateY(180deg);
      font-size: 16px;
      line-height: 1.4em;
      text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== Contenido de las tarjetas =====
    preguntas = [
        "¿COMO ME INSCRIBO EN UN CURSO?",
        "¿Qué significa RLS en Supabase?",
        "Explicá la diferencia entre Caspio y Streamlit.",
        "¿Cómo se activa un policy en Supabase?",
        "¿Qué comando usás para cachear datos en Streamlit?",
        "¿Qué es una función SECURITY DEFINER?"
    ]
    
    respuestas = [
        "Tenés que seleccionar el botón FORMULARIO INDEC. "
        "Luego elegís la actividad en la cual querés inscribirte y completás los datos requeridos.",
        "Row Level Security: seguridad a nivel de filas.",
        "Caspio es no-code; Streamlit requiere programar en Python.",
        "Con ALTER TABLE ... ENABLE ROW LEVEL SECURITY y luego CREATE POLICY.",
        "respuesta",
        "respuesta"
    ]
    
    # ===== Renderizar en 2 filas de 3 =====
    for fila in range(2):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = fila * 3 + i
            with col:
                st.markdown(f"""
                <div class="flip-card">
                  <div class="flip-card-inner">
                    <div class="flip-card-front">
                      {preguntas[idx]}
                    </div>
                    <div class="flip-card-back">
                      {respuestas[idx]}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
