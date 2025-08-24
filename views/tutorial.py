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
      font-size: 14px;
      line-height: 1.4em;
      text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== Contenido de las tarjetas =====
    preguntas = [f"Pregunta {i}" for i in range(1, 7)]
    respuestas = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus.",
        "Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.",
        "Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue.",
        "Suspendisse potenti. Ut sed lectus nec sapien fringilla sagittis vitae eget nunc.",
        "Praesent dapibus, neque id cursus faucibus, tortor neque egestas auguae.",
        "Donec sit amet eros. Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
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
