import string
from typing import Type

from sqlalchemy import create_engine, text, desc
from sqlalchemy.orm import Session, sessionmaker

import OlimpiadasDB
from OlimpiadasDB import Olimpiada, Deporte, Evento, Atleta


class Utils:

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
            raise Exception(Utils.OPCION_INCORRECTA)

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
                raise Exception(Utils.OPCION_INCORRECTA)

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
                raise Exception(Utils.OPCION_INCORRECTA)

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
            raise Exception(Utils.OPCION_INCORRECTA)

    @staticmethod
    def buscar_deportista(sesion: Session) -> Atleta:
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
                raise Exception(Utils.OPCION_INCORRECTA)

        else:
            print("MOGAMBO")
        #      TODO: CREAR SI NO EXISTE

        raise Exception("No se pudo encontrar el deportista")

