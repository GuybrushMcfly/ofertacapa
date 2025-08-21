import re
import datetime

# ----------------------------
# Validaciones
# ----------------------------
def validar_cuil(cuil: str) -> bool:
    """
    Verifica que el CUIL tenga 11 dígitos numéricos válidos
    """
    return cuil.isdigit() and len(cuil) == 11

def validar_email(email: str) -> bool:
    """
    Verifica que el email tenga formato válido
    """
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

# ----------------------------
# Utilidades de cursos
# ----------------------------
def clasificar_duracion(dias: int) -> str:
    """
    Devuelve una etiqueta según la duración de un curso
    """
    if dias <= 2:
        return "Corta"
    elif dias <= 5:
        return "Media"
    else:
        return "Larga"

def normalizar_titulo(titulo: str) -> str:
    """
    Convierte el título a mayúsculas (para almacenar homogéneo)
    """
    return titulo.upper().strip() if titulo else ""

def formatear_fecha(fecha: datetime.date) -> str:
    """
    Convierte una fecha a formato DD/MM/YYYY (texto)
    """
    if not fecha:
        return ""
    return fecha.strftime("%d/%m/%Y")
