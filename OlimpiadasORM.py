import enum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum, BLOB, Double
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

class Deporte(base):
    __tablename__ = "deporte"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(String)
    eventos = relationship('Evento', back_populates='deportes')

class Atleta(base):
    __tablename__ = "atleta"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(String)
    sex = Column(String)
    alt = Column(Integer)
    peso = Column(Double)
    participaciones = relationship('Participacion', back_populates='atletas')

class Equipo(base):
    __tablename__ = "equipo"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(String)
    noc = Column(String)
    participaciones = relationship('Participacion', back_populates='equipos')

class Olimpiada(base):
    __tablename__ = "olimpiada"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    games = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    city = Column(String, nullable=False)
    eventos = relationship('Evento', back_populates='olimpiadas')

class Evento(base):
    __tablename__ = "evento"
    id = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String)
    olimpiada = Column(Integer, ForeignKey("olimpiada.id"), primary_key=True)
    deporte = Column(Integer, ForeignKey("deporte.id"), primary_key=True, nullable=False)
    olimpiadas = relationship('Olimpiada', back_populates='eventos')
    deportes = relationship('Deporte', back_populates='eventos')
    participaciones = relationship("Participacion", back_populates="eventos")

class Participacion(base):
    __tablename__ = "participacion"
    atleta = Column(Integer, ForeignKey("atleta.id"), primary_key=True, nullable=False)
    evento = Column(Integer, ForeignKey("evento.id"), primary_key=True, nullable=False)
    equipo = Column(Integer, ForeignKey("equipo.id"), nullable=False)
    edad = Column(Integer, nullable=True, default=None)
    medalla = Column(String, nullable=True, default=None)
    atletas = relationship("Atleta", back_populates="participaciones")
    eventos = relationship("Evento", back_populates="participaciones")
    equipos = relationship("Equipo", back_populates="participaciones")