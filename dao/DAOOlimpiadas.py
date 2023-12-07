import string
from enum import Enum
from typing import Type

from sqlalchemy import create_engine, text, desc
from sqlalchemy.orm import Session, sessionmaker

import OlimpiadasORM
from OlimpiadasORM import Olimpiada, Deporte, Evento, Atleta, Participacion, Equipo


class DAOOlimpiadas:
    class Medalla(Enum):
        ORO = "GOLD"
        PLATA = "SILVER"
        BRONCE = "BRONZE"

        @staticmethod
        def list():
            return list(map(lambda c: c.value, DAOOlimpiadas.Medalla))

    OPCION_INCORRECTA = "Opcion incorrecta"

    @staticmethod
    def sesion_bbdd() -> Session:
        Motor = create_engine("sqlite:///db/olimpiadas.db")

        Sesion = sessionmaker(bind=Motor)
        s = Sesion()

        s.execute(text("PRAGMA foreign_keys = ON;"))
        return s

    @staticmethod
    def seleccion_temporada() -> string:
        temporadaElegida = input("Elija la temporada:\n\t1. Verano\n\t2. Invierno")
        if temporadaElegida == "1":
            return "Summer"
        elif temporadaElegida == "2":
            return "Winter"
        else:
            raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

    @staticmethod
    def seleccion_edicion(session: Session, temporada=None) -> Olimpiada:
        q = session.query(Olimpiada).order_by(desc(Olimpiada.year))
        ediciones = None
        if temporada:
            ediciones = q.filter(Olimpiada.season == temporada)
        else:
            ediciones = q.all()

        if ediciones:
            print("Elija la edición:")
            for idx, ed in enumerate(ediciones):
                print(f"\t{idx + 1} - {ed.city} {ed.year}")
            num_ed = input("Inserte el número de la edición: ")
            try:
                indice = int(num_ed) - 1
                return ediciones[indice]
            except Exception as e:
                raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        raise Exception("No se pudo encontrar la edición")

    @staticmethod
    def seleccion_edicion_por_deportista(deportista: Atleta, temporada=None) -> Olimpiada:
        s_ediciones = set()
        if deportista:
            for part in deportista.participaciones:
                s_ediciones.add(part.eventos.olimpiadas)

        ediciones = list(s_ediciones)

        if len(ediciones) > 0:
            print("Elija la edición:")
            for idx, ed in enumerate(ediciones):
                print(f"\t{idx + 1} - {ed.city} {ed.year}")
            num_ed = input("Inserte el número de la edición: ")
            try:
                indice = int(num_ed) - 1
                return ediciones[indice]
            except Exception as e:
                raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        raise Exception("No se pudo encontrar la edición")

    @staticmethod
    def seleccion_deporte(olimpiada: Olimpiada) -> Deporte:

        deportes = sorted(list(set(map(lambda ev: ev.deportes, olimpiada.eventos))), key=lambda dep: dep.nombre)

        if deportes:
            print("Elija el deporte:")

            for idx, de in enumerate(deportes):
                print(f"\t{idx + 1} - {de.nombre}")
            num_de = input("Inserte el número del deporte: ")
            try:
                indice = int(num_de) - 1
                return deportes[indice]
            except Exception as e:
                raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        raise Exception("No se pudo encontrar el deporte")

    @staticmethod
    def seleccion_evento(deporte: Deporte, olimpiada: Olimpiada=None) -> Type[Evento]:
        eventos = deporte.eventos
        if olimpiada:
            eventos = list(filter(lambda ev: ev.olimpiada == olimpiada.id, deporte.eventos))

        if eventos:
            print("Elija el evento:")
        for idx, ev in enumerate(eventos):
            print(f"\t{idx + 1} - {ev.nombre}")
        num_ev = input("Inserte el número del evento: ")
        try:
            indice = int(num_ev) - 1
            return eventos[indice]
        except Exception as e:
            raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

    @staticmethod
    def buscar_deportista(sesion: Session, creacion=False) -> Atleta:
        namae = input("Introduzca el nombre del deportista: ")

        q = sesion.query(Atleta)
        deportistas = None
        if namae:
            deportistas = q.filter(Atleta.nombre.ilike(f"%{namae}%"))
        else:
            deportistas = q.all()

        if deportistas and deportistas.count() > 0:
            print("Elija el deportista:")
            for idx, de in enumerate(deportistas):
                print(f"\t{idx + 1} - {de.nombre}")
            num_de = input("Inserte el número del deportista: ")
            try:
                indice = int(num_de) - 1
                return deportistas[indice]
            except Exception as e:
                raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        elif creacion:
            return DAOOlimpiadas.crear_deportista(sesion)

        return None

    @staticmethod
    def crear_deportista(sesion: Session) -> Atleta:
        try:
            crear_confirm = input("No existe el deportista; ¿desea crear uno nuevo? S/N")[0].upper()
            if crear_confirm != "S":
                return

            nombre = input("Introduzca el nombre del deportista: ")

            sexo = input("Introduzca el sexo (M/F): ")[0].upper()

            if sexo not in ["M", "F"]:
                print("Sexo inválido")
                return

            altura = int(input("Introduzca la altura en centímetros: "))
            peso = float(input("Introduzca el peso (Kg): "))

            nuevo_atleta = Atleta()
            nuevo_atleta.nombre = nombre
            nuevo_atleta.alt = altura
            nuevo_atleta.peso = peso
            nuevo_atleta.sex = sexo

            sesion.add(nuevo_atleta)
            sesion.commit()
            print("Se creó el deportista")
            sesion.refresh(nuevo_atleta)
            return nuevo_atleta
        except Exception as e:
            sesion.rollback()
            print("ERROR: No se pudo crear el deportista.")
        return None

    @staticmethod
    def buscar_participacion(deportista: Atleta) -> Participacion:
        participaciones: list[Participacion] = deportista.participaciones

        if participaciones:
            print("Elija el evento:")
            for idx, part in enumerate(participaciones):
                evento: Evento = part.eventos
                print(f"\t{idx + 1} - {evento.nombre}")

            num_par = input("Inserte el número del evento: ")
            try:
                indice = int(num_par) - 1
                return participaciones[indice]
            except Exception as e:
                raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        return None

    @staticmethod
    def actualizar_medalla(participacion: Participacion):
        print("Elija la medalla:")
        valor_medalla = None
        for idx, med in enumerate(DAOOlimpiadas.Medalla.list()):
            print(f"{idx + 1} - {med}")
        print("4 - Ninguna")
        num_med = input("Inserte el número de la medalla: ")
        try:
            if num_med != "4":
                indice = int(num_med) - 1
                valor_medalla = DAOOlimpiadas.Medalla.list()[indice]
        except Exception as e:
            raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        participacion.medalla = valor_medalla

    @staticmethod
    def elegir_equipo(sesion: Session) -> Equipo:
        print("Elija el equipo:")
        equipos: list[Equipo] = sesion.query(Equipo).order_by(Equipo.nombre).all()
        for idx, eq in enumerate(equipos):
            print(f"{idx + 1} - {eq.nombre} ({eq.noc})")

        num_eq = input("Inserte el número del equipo: ")
        try:
                indice = int(num_eq) - 1
                return equipos[indice]
        except Exception as e:
            raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)

        raise Exception("No se encontró el equipo")
