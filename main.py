from OlimpiadasORM import Atleta, Participacion, Equipo
from dao import DAOOlimpiadas
from dao.DAOOlimpiadas import DAOOlimpiadas


class Renkinjutsu:
    def __init__(self):
        menu = """
        Elija una opción:
            1. Listado de deportistas participantes
            2. Modificar medalla
            3. Añadir deportista/participación
            4. Eliminar participación
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
            if opcion == "4":
                self.__ejercicio4__()



    def __ejercicio1__(self):
        session = None
        try:
            session = DAOOlimpiadas.sesion_bbdd()
            temporada = DAOOlimpiadas.seleccion_temporada()
            edicion = DAOOlimpiadas.seleccion_edicion(session, temporada=temporada)
            deporte = DAOOlimpiadas.seleccion_deporte(edicion)
            evento = DAOOlimpiadas.seleccion_evento(deporte, olimpiada=edicion)

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
            session = DAOOlimpiadas.sesion_bbdd()
            deportista = DAOOlimpiadas.buscar_deportista(session)
            if not deportista:
                print("No se hallaron resultados.")
                return
            participacion = DAOOlimpiadas.buscar_participacion(deportista)
            if not participacion:
                print("No existe la participación.")
                return
            DAOOlimpiadas.actualizar_medalla(participacion)
            session.commit()
        except Exception as e:
            print(e)
        finally:
            if session:
                session.close()

    def __ejercicio3__(self):
        session = None
        try:
            session = DAOOlimpiadas.sesion_bbdd()

            deportista = DAOOlimpiadas.buscar_deportista(session, creacion=True)
            if deportista:
                temporada = DAOOlimpiadas.seleccion_temporada()
                edicion = DAOOlimpiadas.seleccion_edicion(session, temporada=temporada)
                deporte = DAOOlimpiadas.seleccion_deporte(edicion)
                evento = DAOOlimpiadas.seleccion_evento(deporte, olimpiada=edicion)
                equipo = DAOOlimpiadas.elegir_equipo(session)

                nueva_participacion = Participacion()
                nueva_participacion.atleta = deportista.id
                nueva_participacion.evento = evento.id
                nueva_participacion.equipo = equipo.id
                nueva_participacion.edad = int(input("Inserte la edad del deportista: "))
                DAOOlimpiadas.actualizar_medalla(nueva_participacion)

                session.add(nueva_participacion)
                session.commit()
            else:
                print("ERROR: No existe el deportista")
        except Exception as e:
            if session:
                session.rollback()
            print(e)
        finally:
            if session:
                session.close()

    def __ejercicio4__(self):
        session = None
        try:
            session = DAOOlimpiadas.sesion_bbdd()

            deportista = DAOOlimpiadas.buscar_deportista(session)
            if not deportista:
                print("ERROR: No existe el deportista")
                return

            #SI NO HAY NINGUNA PARTICIPACIÓN, TAMBIÉN ME CARGO AL DEPORTISTA
            if len(deportista.participaciones) < 2:
                # NO PUSE ON DELETE CASCADE AL CREARLA :(
                if len(deportista.participaciones) == 1:
                    session.delete(deportista.participaciones[0])
                session.delete(deportista)
                print("El deportista y su participación furon eliminados")
            else:
                participacion = DAOOlimpiadas.buscar_participacion(deportista)
                if not participacion:
                    print("ERROR: No existe la participación")
                    return
                session.delete(participacion)
                print("La participación fue eliminada")

            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            print(e)
        finally:
            if session:
                session.close()



Renkinjutsu()