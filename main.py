from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from OlimpiadasDB import Deporte, Atleta, Participacion, Equipo, Evento
from Utils import Utils


class Renkinjutsu:
    def __init__(self):
        menu = """
        Elija una opción:
            1. Listado de deportistas participantes
            2. Modificar medalla
            3. Añadir deportista/participación
            0. Salir
        """

        opcion = None
        while opcion != "0":
            opcion = input(menu)
            if opcion == "1":
                self.__ejercicio1__()
            if opcion == "2":
                self.__ejercicio2__()
            if opcion == "3":
                self.__ejercicio3__()



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
            deportista = Utils.buscar_deportista(session)
            if not deportista:
                print("No se hallaron resultados.")
                return
            participacion = Utils.buscar_participacion(deportista)
            if not deportista:
                print("No existe la participación.")
                return
            Utils.actualizar_medalla(participacion)
            session.commit()
        except Exception as e:
            print(e)
        finally:
            if session:
                session.close()

    def __ejercicio3__(self):
        session = None
        try:
            session = Utils.sesion_bbdd()
            deportista = Utils.buscar_deportista(session, creacion=True)

            temporada = Utils.seleccion_temporada()
            edicion = Utils.seleccion_edicion_por_deportista(deportista, temporada=temporada)

            # TODO: Continuar por aquí


        except Exception as e:
            if session:
                session.rollback()
            print(e)
        finally:
            if session:
                session.close()

Renkinjutsu()