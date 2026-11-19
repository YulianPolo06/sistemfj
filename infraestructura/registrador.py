"""Capa de infraestructura: registro de eventos y errores en archivo de logs."""

import os
from datetime import datetime


class Registrador:
    """Escribe eventos y errores en logs/sistema.log (sin base de datos)."""

    def __init__(self, ruta=None):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__ruta = ruta or os.path.join(base, "logs", "sistema.log")
        os.makedirs(os.path.dirname(self.__ruta), exist_ok=True)

    @property
    def ruta(self):
        return self.__ruta

    def __escribir(self, nivel, texto):
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = "[{0}] {1} - {2}\n".format(marca, nivel, texto)
        try:
            with open(self.__ruta, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error:
            # Si falla el log, el sistema no debe caer.
            print("No se pudo escribir en el log:", error)
        return linea

    def evento(self, texto):
        return self.__escribir("EVENTO", texto)

    def advertencia(self, texto):
        return self.__escribir("ADVERTENCIA", texto)

    def error(self, excepcion, contexto="operacion"):
        tipo = type(excepcion).__name__
        causa = excepcion.__cause__
        detalle = "{0} | {1}: {2}".format(contexto, tipo, excepcion)
        if causa is not None:
            detalle += " | causado por {0}: {1}".format(type(causa).__name__, causa)
        return self.__escribir("ERROR", detalle)

    def leer(self):
        try:
            with open(self.__ruta, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except FileNotFoundError:
            return "Aun no hay registros en el archivo de logs."

    def limpiar(self):
        try:
            open(self.__ruta, "w", encoding="utf-8").close()
        except OSError as error:
            print("No se pudo limpiar el log:", error)
