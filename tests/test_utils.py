from utils.validators import validar_rut


def test_validar_rut():
    assert validar_rut('12345678-9')
    assert not validar_rut('1234')
