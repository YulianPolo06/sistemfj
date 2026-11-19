"""Capa de excepciones personalizadas del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepcion base. Todas las demas heredan de ella."""

    def __init__(self, mensaje="Error no especificado en el sistema"):
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato no cumple las validaciones."""


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un parametro obligatorio."""


class ClienteDuplicadoError(ErrorSistemaFJ):
    """Se lanza al registrar un cliente con documento ya existente."""


class EntidadNoEncontradaError(ErrorSistemaFJ):
    """Se lanza cuando no existe el cliente, servicio o reserva solicitado."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inhabilitado."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante una reserva mal construida o en estado incorrecto."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al ejecutar una operacion no valida para el estado actual."""


class CalculoCostoError(ErrorSistemaFJ):
    """Se lanza cuando el calculo de costos resulta inconsistente."""
