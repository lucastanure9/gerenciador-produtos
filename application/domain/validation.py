from datetime import datetime

class OperationCancelled(Exception):
    """Indica que o usuário cancelou a operação digitando 'sair'."""
    pass


def validar_int(txt):
    try:
        return int(txt)
    except ValueError:
        return None


def validar_nome(txt):
    t = txt.strip()
    return t if t else None


def validar_preco(txt):
    t = txt.strip().replace(',', '.')
    try:
        p = float(t)
        return p if p > 0 else None
    except ValueError:
        return None


def validar_data(txt):
    t = txt.strip().replace('/', '-')
    if not t:
        return None
    try:
        datetime.strptime(t, "%d-%m-%Y")
        return t
    except ValueError:
        return None