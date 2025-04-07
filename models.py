from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Modelo de Veterinario
class Veterinario(Base):
    __tablename__ = "veterinarios"
    
    rut_veterinario = Column(String(255), primary_key=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    especializacion = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)  # Contraseña en texto plano
    # Relación con Mascota (Un veterinario puede atender varias mascotas)
    mascotas = relationship("Mascota", back_populates="veterinario")

# Modelo de Mascota
class Mascota(Base):
    __tablename__ = "mascotas"
    
    chapa = Column(String(255), primary_key=True)  
    nombre = Column(String(255), nullable=False)
    raza = Column(String(255), nullable=False)
    sexo = Column(String(255), nullable=False)
    dieta = Column(String(255), nullable=False)
    caracter = Column(String(255), nullable=False)
    habitat = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    peso = Column(String(255), nullable=False)
    altura = Column(String(255), nullable=False)
    rut_veterinario = Column(String(255), ForeignKey("veterinarios.rut_veterinario"), nullable=True)

    # Relación con Veterinario
    veterinario = relationship("Veterinario", back_populates="mascotas")
