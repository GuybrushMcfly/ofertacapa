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
      font-size: 20px;
      font-weight: bold;
    }
    .flip-card-back {
      background-color: #f9f9f9;
      color: #333;
      transform: rotateY(180deg);
      font-size: 18px;
      line-height: 1.4em;
      text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== Contenido de las tarjetas =====
    preguntas = [
        "¿DÓNDE ENCUENTRO LOS CURSOS DISPONIBLES PARA INSCRIBIRME?",
        "¿CÓMO ME INSCRIBO EN UN CURSO?",
        "¿TENGO QUE HACER DOBLE INSCRIPCIÓN?",
        "¿QUIERO INSCRIBIRME PERO EL FORMULARIO NO PERMITE?",
        "¿CUÁNDO RECIBO LA VACANTE DE LAS ACTIDADES SOLICITADAS?",
        "¿Qué es una función SECURITY DEFINER?"
    ]
    
    respuestas = [
        #respuesta "¿DÓNDE ENCUENTRO LAS ACTIVIDADES DISPONIBLES PARA INSCRIBIRME?"
        "Tanto en el botón DESTACADOS como en el LISTADO OFERTAS vas a encontrar las actividades disponibles. "
        "Todas las semanas se irán actualizando las ofertas.",
        
        #respuesta "¿CÓMO ME INSCRIBO EN UN CURSO?"
        "Tenés que cliquear en el botón FORMULARIO INDEC. "
        "Luego elegís la actividad en la cual querés inscribirte y completás los datos requeridos.",

        #respuesta "¿TENGO QUE HACER DOBLE INSCRIPCIÓN?"
        "SI. Solamente en las actividades de INAP tenés que inscribirte tanto en INAP como en el FORMULARIO INDEC. "
        "Esta doble inscripción garantiza un mejor control de las inscripciones y vacantes.",
    
        #respuesta "¿TENGO QUE HACER DOBLE INSCRIPCIÓN?""¿QUIERO INSCRIBIRME PERO EL FORMULARIO NO PERMITE?",
        "Al seleccionar una actividad vas a tener que validar tus datos. Si no te permite continuar: "
        "a) verificá tu CUIL/CUIL, b) ya te inscribiste en esa actividad, c) ya aprobaste esa actividad anteriormente.",

        #respuesta "¿CUÁNDO RECIBO LA VACANTE DE LAS ACTIVIDADES SOLICITADAS?"    
        "La noticación de la vacante te puede llegar a tu correo incluso el mismo día que comienza la actividad."
        "IMPORTANTE!! Recordá que haberte inscripto en una actividad no garantiza la asignación de vacante.",
    
        "Una función <b>SECURITY DEFINER</b> se ejecuta con los privilegios del creador, no del invocador."
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
