"""Servicio especializado: alquiler de equipos."""

import math

from dominio.servicio import Servicio
from excepciones.errores import DatosInvalidosError, ReservaInvalidaError


class AlquilerEquipo(Servicio):
    """Cobro por dia; la duracion recibida en horas se convierte a dias."""

    HORAS_POR_DIA = 8

    def __init__(self, nombre, tarifa_base, cantidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self.cantidad = cantidad

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor):
        try:
            unidades = int(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La cantidad de equipos '{0}' no es un entero".format(valor)
            ) from error
        if unidades < 1:
            raise DatosInvalidosError("Debe existir al menos un equipo disponible")
        self.__cantidad = unidades

    def unidad_duracion(self):
        return "dia"

    def validar_parametros(self, duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError("La duracion del alquiler no es valida") from error
        if horas <= 0:
            raise ReservaInvalidaError("El alquiler debe tener una duracion positiva")
        if horas > AlquilerEquipo.HORAS_POR_DIA * 30:
            raise ReservaInvalidaError("El alquiler no puede superar los 30 dias")
        return True

    def calcular_costo(self, duracion):
        dias = math.ceil(float(duracion) / AlquilerEquipo.HORAS_POR_DIA)
        return self.tarifa_base * max(dias, 1)

    def descripcion(self):
        return "{0} | {1} unidades en inventario".format(super().descripcion(), self.cantidad)
