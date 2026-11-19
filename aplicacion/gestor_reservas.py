"""Capa de aplicacion: gestion de reservas en memoria."""

from dominio.reserva import Reserva
from excepciones.errores import EntidadNoEncontradaError


class GestorReservas:
    def __init__(self, registrador):
        self.__reservas = []
        self.__registrador = registrador

    @property
    def reservas(self):
        return tuple(self.__reservas)

    def crear(self, cliente, servicio, duracion, confirmar=True):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            if confirmar:
                reserva.confirmar()
        except Exception as error:
            self.__registrador.error(error, "creacion de reserva")
            raise
        else:
            self.__reservas.append(reserva)
            self.__registrador.evento("Reserva creada {0}".format(reserva.resumen()))
            return reserva

    def buscar(self, identificador):
        texto = str(identificador).strip()
        for reserva in self.__reservas:
            if reserva.identificador == texto:
                return reserva
        error = EntidadNoEncontradaError("No existe la reserva '{0}'".format(identificador))
        self.__registrador.error(error, "busqueda de reserva")
        raise error

    def confirmar(self, identificador):
        reserva = self.buscar(identificador)
        try:
            reserva.confirmar()
        except Exception as error:
            self.__registrador.error(error, "confirmacion de {0}".format(identificador))
            raise
        self.__registrador.evento("Reserva confirmada {0}".format(identificador))
        return reserva

    def cancelar(self, identificador, motivo="solicitud del cliente"):
        reserva = self.buscar(identificador)
        try:
            reserva.cancelar(motivo)
        except Exception as error:
            self.__registrador.error(error, "cancelacion de {0}".format(identificador))
            raise
        self.__registrador.evento(
            "Reserva cancelada {0} ({1})".format(identificador, motivo)
        )
        return reserva

    def procesar(self, identificador, descuento=None, impuesto=None):
        reserva = self.buscar(identificador)
        try:
            total = reserva.procesar(descuento, impuesto)
        except Exception as error:
            self.__registrador.error(error, "procesamiento de {0}".format(identificador))
            raise
        else:
            self.__registrador.evento(
                "Reserva procesada {0} por {1:,.2f}".format(identificador, total)
            )
            return total

    def total_facturado(self):
        return round(sum(reserva.costo for reserva in self.__reservas), 2)

    def listar(self):
        return [reserva.resumen() for reserva in self.__reservas]
