from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Persona(Base):
    __tablename__ = 'persona'
    rut = Column(String(50), primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    edad = Column(Integer)
    email = Column(String(50))
    tipo = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'persona',
        'polymorphic_on': tipo
    }

class Admin(Persona):
    __tablename__ = 'admin'
    id_admin = Column(Integer, primary_key=True)
    contrasena = Column(String(50))
    rut = Column(String(50), ForeignKey('persona.rut'), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

class Recepcionista(Persona):
    __tablename__ = 'recepcionista'
    id_recepcionista = Column(Integer, primary_key=True)
    contrasena = Column(String(50))
    rut = Column(String(50), ForeignKey('persona.rut'), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'recepcionista',
    }

class Cliente(Persona):
    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key=True)
    id_mascota = Column(Integer, ForeignKey('mascota.id_mascota'))
    rut = Column(String(50), ForeignKey('persona.rut'), unique=True)

    mascota = relationship("Mascota")

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

class Veterinario(Persona):
    __tablename__ = 'veterinario'
    id_vet = Column(Integer, primary_key=True)
    especializacion = Column(String(255))
    contrasena = Column(String(255))
    rut = Column(String(50), ForeignKey('persona.rut'), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'veterinario',
    }

class Mascota(Base):
    __tablename__ = 'mascota'

    id_mascota = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    raza = Column(String)
    sexo = Column(String)
    dieta = Column(String)
    caracter = Column(String)
    habitat = Column(String)
    edad = Column(Integer)
    peso = Column(String)
    altura = Column(String)
    id_vet = Column(Integer, ForeignKey('veterinario.id_vet'), nullable=True)

class Consulta(Base):
    __tablename__ = 'consulta'
    id_consulta = Column(Integer, primary_key=True)
    id_recepcionista = Column(Integer, ForeignKey('recepcionista.id_recepcionista'))
    id_mascota = Column(Integer, ForeignKey('mascota.id_mascota'))
    id_vet = Column(Integer, ForeignKey('veterinario.id_vet'))
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))
    motivo = Column(String(255))

    recepcionista = relationship("Recepcionista")
    mascota = relationship("Mascota")
    veterinario = relationship("Veterinario")
    cliente = relationship("Cliente")

def create_tables(engine):
    Base.metadata.create_all(engine)
