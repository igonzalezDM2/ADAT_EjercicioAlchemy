import string
from enum import Enum
from typing import Type, Callable, Any

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

        return DAOOlimpiadas.elegir_opcion(ediciones, lambda idx, ed: f"\t{idx + 1} - {ed.city} {ed.year}", "edición")

    @staticmethod
    def seleccion_edicion_por_deportista(deportista: Atleta, temporada=None) -> Olimpiada:
        s_ediciones = set()
        if deportista:
            for part in deportista.participaciones:
                s_ediciones.add(part.eventos.olimpiadas)

        ediciones = list(s_ediciones)

        if len(ediciones) > 0:
            return DAOOlimpiadas.elegir_opcion(ediciones, lambda idx, ed: f"\t{idx + 1} - {ed.city} {ed.year}", "edición")

        raise Exception("No se pudo encontrar la edición")

    @staticmethod
    def seleccion_deporte(olimpiada: Olimpiada) -> Deporte:
        deportes = sorted(list(set(map(lambda ev: ev.deportes, olimpiada.eventos))), key=lambda dep: dep.nombre)

        if deportes:
            return DAOOlimpiadas.elegir_opcion(deportes, lambda idx, de: f"\t{idx + 1} - {de.nombre}", "deporte")

        raise Exception("No se pudo encontrar el deporte")

    @staticmethod
    def seleccion_evento(deporte: Deporte, olimpiada: Olimpiada=None) -> Type[Evento]:
        eventos = deporte.eventos
        if olimpiada:
            eventos = list(filter(lambda ev: ev.olimpiada == olimpiada.id, deporte.eventos))

        if eventos:
            return DAOOlimpiadas.elegir_opcion(eventos, lambda idx, ev: f"\t{idx + 1} - {ev.nombre}", "evento")
        raise Exception("No se pudo encontrar el evento")

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
            return DAOOlimpiadas.elegir_opcion(deportistas, lambda idx, de: f"\t{idx + 1} - {de.nombre}", "deportista")
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
            return DAOOlimpiadas.elegir_opcion(participaciones, lambda idx, part: f"\t{idx + 1} - {part.eventos.nombre}", "evento")

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
        return DAOOlimpiadas.elegir_opcion(equipos, lambda idx, eq: f"{idx + 1} - {eq.nombre} ({eq.noc})", "equipo")

    @staticmethod
    def elegir_opcion(lista: list, print_callback: Callable[[int, Any], str], tipo_objeto="") -> Any:
        print(f"Elija {tipo_objeto}:")
        for idx, el in enumerate(lista):
            print(print_callback(idx, el))

        num_el = input(f"Inserte el número de {tipo_objeto}: ")
        try:
                indice = int(num_el) - 1
                return lista[indice]
        except Exception as e:
            raise Exception(DAOOlimpiadas.OPCION_INCORRECTA)
