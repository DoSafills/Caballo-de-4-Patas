class UsuarioIterator:
    def __init__(self, usuarios):
        self._usuarios = usuarios
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._usuarios):
            usuario = self._usuarios[self._index]
            self._index += 1
            return usuario
        else:
            raise StopIteration

class ColeccionUsuarios:
    def __init__(self, usuarios):
        self._usuarios = usuarios

    def __iter__(self):
        return UsuarioIterator(self._usuarios)