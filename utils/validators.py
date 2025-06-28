import re


def validar_rut(rut: str) -> bool:
    return bool(re.match(r"^[0-9]{7,8}-[0-9kK]$", rut))
