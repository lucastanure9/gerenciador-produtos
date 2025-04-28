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
    try:
        p = float(txt)
        return p if p >= 0 else None
    except ValueError:
        return None

def validar_data(txt):
    t = txt.strip()
    if not t:
        return None
    try:
        datetime.strptime(t, "%d-%m-%Y")
        return t
    except ValueError:
        return None

def solicitar_input(prompt, validator, permitir_vazio=False):
    """
    Prompt repetido até ter valor válido ou o usuário digitar 'sair'.
    - prompt: string para input()
    - validator: função que recebe string, retorna valor convertido ou None
    - permitir_vazio: se True, ENTER vazio retorna None sem validar
    """
    while True:
        txt = input(prompt).strip()
        if txt.lower() == 'sair':
            raise OperationCancelled()
        if permitir_vazio and txt == '':
            return None
        val = validator(txt)
        if val is not None:
            return val
        print("Entrada inválida. Tente novamente ou digite 'sair' para cancelar.")