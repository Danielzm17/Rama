from datetime import datetime

def validar_numero_real(numero):
    try:
        float(numero)
        return True
    except ValueError:
        return False
    except Exception as e:
        return False


def validar_numero_entero(numero):
    try:
        int(numero)
        return True
    except ValueError:
        return False
    except Exception as e:
        return False


def validar_si_es_texto(texto):
    return isinstance(texto, str)


def validar_texto_vacio(texto):
    if validar_si_es_texto(texto):
        if len(texto.strip()) == 0:
            return True
        else:
            return False
    else:
        return None

def validar_fecha_iso8601(fecha):
    try:
        datetime.fromisoformat(fecha)
        return True
    except ValueError:
        return False