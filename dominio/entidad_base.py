"""Clase abstracta general para todas las entidades del sistema."""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """Abstraccion de cualquier entidad (clientes, servicios, reservas)."""

    _consecutivo = 0

    def __init__(self, prefijo="ENT"):
        EntidadBase._consecutivo += 1
        self.__identificador = "{0}-{1:03d}".format(prefijo, EntidadBase._consecutivo)
        self.__creado_en = datetime.now()

    @property
    def identificador(self):
        return self.__identificador

    @property
    def creado_en(self):
        return self.__creado_en

    @abstractmethod
    def descripcion(self):
        """Cada entidad describe su informacion de forma polimorfica."""

    @abstractmethod
    def validar(self):
        """Cada entidad valida su propio estado y lanza excepciones si falla."""

    def resumen(self):
        return "{0} | {1}".format(self.identificador, self.descripcion())

    def __str__(self):
        return self.resumen()
