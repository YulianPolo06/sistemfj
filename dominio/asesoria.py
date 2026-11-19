"""Servicio especializado: asesorias profesionales."""

from dominio.servicio import Servicio
from excepciones.errores import DatosInvalidosError, ReservaInvalidaError


class Asesoria(Servicio):
    """Cobro por hora con multiplicador segun el nivel del asesor."""

    NIVELES = {"basico": 1.0, "intermedio": 1.3, "experto": 1.8}
    MINIMO_HORAS = 2

    def __init__(self, nombre, tarifa_base, nivel, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self.nivel = nivel

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        texto = str(valor).strip().lower() if valor is not None else ""
        if texto not in Asesoria.NIVELES:
            raise DatosInvalidosError(
                "Nivel '{0}' invalido. Opciones: {1}".format(
                    valor, ", ".join(Asesoria.NIVELES)
                )
            )
        self.__nivel = texto

    def unidad_duracion(self):
        return "hora"

    def validar_parametros(self, duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError("La duracion de la asesoria no es valida") from error
        if horas < Asesoria.MINIMO_HORAS:
            raise ReservaInvalidaError(
                "La asesoria exige minimo {0} horas".format(Asesoria.MINIMO_HORAS)
            )
        if horas > 20:
            raise ReservaInvalidaError("La asesoria no puede exceder 20 horas")
        return True

    def calcular_costo(self, duracion):
        horas = float(duracion)
        return self.tarifa_base * horas * Asesoria.NIVELES[self.nivel]

    def descripcion(self):
        return "{0} | nivel {1}".format(super().descripcion(), self.nivel)
