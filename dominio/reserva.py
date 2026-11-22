"""Entidad Reserva: integra cliente, servicio, duracion y estado."""

from dominio.cliente import Cliente
from dominio.entidad_base import EntidadBase
from dominio.servicio import Servicio
from excepciones.errores import (
    CalculoCostoError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
)


class Reserva(EntidadBase):
    """Ciclo de vida: PENDIENTE -> CONFIRMADA -> PROCESADA | CANCELADA."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion):
        super().__init__(prefijo="RES")
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere cliente y servicio")
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente asociado no es valido")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio asociado no es valido")

        self.__cliente = cliente
        self.__servicio = servicio
        self.duracion = duracion
        self.__estado = Reserva.PENDIENTE
        self.__costo = 0.0
        self.__observaciones = []

    # ------------------ propiedades ------------------
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        try:
            cantidad = float(valor)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError(
                "La duracion '{0}' no es numerica".format(valor)
            ) from error
        if cantidad <= 0:
            raise ReservaInvalidaError("La duracion debe ser mayor que cero")
        self.__duracion = cantidad

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    @property
    def observaciones(self):
        return tuple(self.__observaciones)

    # ------------------ comportamiento ------------------
    def confirmar(self):
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                "Solo se confirman reservas pendientes (estado actual: {0})".format(self.__estado)
            )
        self.__servicio.verificar_disponibilidad()
        self.__servicio.validar_parametros(self.__duracion)
        self.__estado = Reserva.CONFIRMADA
        self.__observaciones.append("Reserva confirmada")
        self.__cliente.agregar_reserva(self)
        return self.__estado

    def cancelar(self, motivo="sin motivo registrado"):
        if self.__estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva {0}".format(self.__estado)
            )
        self.__estado = Reserva.CANCELADA
        self.__observaciones.append("Cancelada: {0}".format(motivo))
        return self.__estado

    def procesar(self, descuento=None, impuesto=None):
        """Calcula el costo final usando el metodo sobrecargado del servicio."""
        if self.__estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "Solo se procesan reservas confirmadas (estado actual: {0})".format(self.__estado)
            )
        if descuento is None:
            descuento = self.__cliente.descuento_aplicable()

        try:
            if impuesto is None:
                total = self.__servicio.calcular_costo_total(self.__duracion, descuento)
            else:
                total = self.__servicio.calcular_costo_total(
                    self.__duracion, descuento=descuento, impuesto=impuesto
                )
        except CalculoCostoError as error:
            self.__observaciones.append("Fallo de calculo: {0}".format(error))
            raise
        except Exception as error:
            # Se traduce cualquier error inesperado a una excepcion del dominio.
            raise CalculoCostoError(
                "Error inesperado procesando la reserva {0}".format(self.identificador)
            ) from error
        else:
            self.__costo = total
            self.__estado = Reserva.PROCESADA
            self.__observaciones.append("Procesada por {0:,.2f}".format(total))
            return total
        finally:
            self.__observaciones.append("Intento de procesamiento finalizado")

    def validar(self):
        self.duracion = self.__duracion
        self.__servicio.validar_parametros(self.__duracion)
        return True

    def descripcion(self):
        return "{0} -> {1} | {2} {3}(s) | estado {4} | costo {5:,.2f}".format(
            self.__cliente.nombre,
            self.__servicio.nombre,
            self.__duracion,
            self.__servicio.unidad_duracion(),
            self.__estado,
            self.__costo,
        )