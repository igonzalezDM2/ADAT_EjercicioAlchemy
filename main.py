from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from OlimpiadasDB import Deporte, Atleta, Participacion, Equipo
from Utils import Utils


class Renkinjutsu:
    def __init__(self):
        menu = """
        Elija una opción:
            1. Listado de deportistas participantes
            2. Añadir deportista/participación
            0. Salir
        """

        opcion = None
        while opcion != "0":
            opcion = input(menu)
            if opcion == "1":
                self.__ejercicio1__()
            if opcion == "2":
                self.__ejercicio2__()



    def __ejercicio1__(self):
        session = None
        try:
            session = Utils.sesion_bbdd()
            temporada = Utils.seleccion_temporada()
            edicion = Utils.seleccion_edicion(session, temporada=temporada)
            deporte = Utils.seleccion_deporte(edicion)
            evento = Utils.seleccion_evento(deporte, olimpiada=edicion)

            print(f"Temporada: {temporada}\nEdición: {edicion.city} {edicion.year}\n Deporte: {deporte.nombre}\nEvento: {evento.nombre}\n")
            participaciones: list[Participacion] = evento.participaciones
            if participaciones:
                for par in participaciones:
                    atleta: Atleta = par.atletas
                    equipo: Equipo = par.equipos
                    print(f"\t{atleta.nombre} - Altura: {atleta.alt}, Peso: {atleta.peso}, Edad: {par.edad}, Equipo: {equipo.nombre}({equipo.noc}) Medalla: {par.medalla if par.medalla else 'NO'}")
        except Exception as e:
            print(e)
        finally:
            if session:
                session.close()

    def __ejercicio2__(self):
        session = None
        try:
            session = Utils.sesion_bbdd()
            Utils.buscar_deportista(session)
        except Exception as e:
            print(e)
        finally:
            if session:
                session.close()

Renkinjutsu()