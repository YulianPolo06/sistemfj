"""Servicio especializado: reserva de salas."""

from dominio.servicio import Servicio
from excepciones.errores import DatosInvalidosError, ReservaInvalidaError


class SalaReuniones(Servicio):
    """Cobro por hora con recargo cuando la sala es de gran capacidad."""

    MAXIMO_HORAS = 10

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self.capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        try:
            cupos = int(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La capacidad '{0}' no es un numero entero".format(valor)
            ) from error
        if not 1 <= cupos <= 100:
            raise DatosInvalidosError("La capacidad debe estar entre 1 y 100 personas")
        self.__capacidad = cupos

    def unidad_duracion(self):
        return "hora"

    def validar_parametros(self, duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError("La duracion en horas no es valida") from error
        if horas <= 0:
            raise ReservaInvalidaError("La sala debe reservarse por al menos 1 hora")
        if horas > SalaReuniones.MAXIMO_HORAS:
            raise ReservaInvalidaError(
                "La sala no puede reservarse mas de {0} horas".format(SalaReuniones.MAXIMO_HORAS)
            )
        return True

    def calcular_costo(self, duracion):
        horas = float(duracion)
        recargo = 1.2 if self.capacidad > 10 else 1.0
        return self.tarifa_base * horas * recargo

    def descripcion(self):
        return "{0} | capacidad {1} personas".format(super().descripcion(), self.capacidad)
