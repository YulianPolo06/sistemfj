"""Clase abstracta Servicio: base de todos los servicios de Software FJ."""

from abc import abstractmethod

from dominio.entidad_base import EntidadBase
from excepciones.errores import (
    CalculoCostoError,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase):
    """Abstraccion de un servicio. Define el contrato que cumplen las subclases."""

    IVA = 0.19

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__(prefijo="SRV")
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.__disponible = bool(disponible)

    # ------------------ propiedades encapsuladas ------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio")
        self.__nombre = str(valor).strip()

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise DatosInvalidosError(
                "La tarifa '{0}' no es un valor numerico".format(valor)
            ) from error
        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero")
        self.__tarifa_base = tarifa

    @property
    def disponible(self):
        return self.__disponible

    def habilitar(self):
        self.__disponible = True

    def inhabilitar(self):
        self.__disponible = False

    def verificar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                "El servicio '{0}' no esta disponible actualmente".format(self.nombre)
            )
        return True

    # ------------------ metodos abstractos (polimorfismo) ------------------
    @abstractmethod
    def calcular_costo(self, duracion):
        """Cada servicio calcula su costo de forma distinta."""

    @abstractmethod
    def unidad_duracion(self):
        """Texto de la unidad usada por el servicio (horas, dias, sesiones)."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida que la duracion solicitada sea aceptable para el servicio."""

    # ------------------ metodo sobrecargado ------------------
    def calcular_costo_total(self, *args, **kwargs):
        """Variantes de calculo (sobrecarga simulada en Python):

        calcular_costo_total(duracion)
        calcular_costo_total(duracion, descuento)
        calcular_costo_total(duracion, descuento, impuesto)
        calcular_costo_total(duracion, descuento=0.1, impuesto=0.19)
        """
        if not args and "duracion" not in kwargs:
            raise ParametroFaltanteError("Debe indicar la duracion del servicio")

        duracion = args[0] if args else kwargs.get("duracion")
        descuento = args[1] if len(args) > 1 else kwargs.get("descuento", 0.0)
        impuesto = args[2] if len(args) > 2 else kwargs.get("impuesto", Servicio.IVA)

        try:
            descuento = float(descuento)
            impuesto = float(impuesto)
        except (TypeError, ValueError) as error:
            raise CalculoCostoError("Descuento e impuesto deben ser numericos") from error

        if not 0.0 <= descuento <= 0.5:
            raise CalculoCostoError("El descuento debe estar entre 0.0 y 0.5")
        if not 0.0 <= impuesto <= 0.5:
            raise CalculoCostoError("El impuesto debe estar entre 0.0 y 0.5")

        self.verificar_disponibilidad()
        self.validar_parametros(duracion)

        subtotal = self.calcular_costo(duracion)
        if subtotal is None or subtotal <= 0:
            raise CalculoCostoError(
                "Calculo inconsistente en '{0}': subtotal {1}".format(self.nombre, subtotal)
            )
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def descripcion(self):
        estado = "disponible" if self.disponible else "inhabilitado"
        return "{0} '{1}' - tarifa {2:,.0f} por {3} ({4})".format(
            type(self).__name__, self.nombre, self.tarifa_base,
            self.unidad_duracion(), estado,
        )

    def validar(self):
        self.nombre = self.__nombre
        self.tarifa_base = self.__tarifa_base
        return True
