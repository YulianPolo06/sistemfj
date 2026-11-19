"""Capa de aplicacion: gestion de clientes en memoria (sin base de datos)."""

from dominio.cliente import Cliente
from excepciones.errores import ClienteDuplicadoError, EntidadNoEncontradaError


class GestorClientes:
    def __init__(self, registrador):
        self.__clientes = []
        self.__registrador = registrador

    @property
    def clientes(self):
        return tuple(self.__clientes)

    def registrar(self, nombre, documento, correo, telefono="", vip=False):
        """Crea y almacena un cliente. Propaga excepciones del dominio."""
        try:
            cliente = Cliente(nombre, documento, correo, telefono, vip)
            if self.buscar_opcional(cliente.documento) is not None:
                raise ClienteDuplicadoError(
                    "Ya existe un cliente con documento {0}".format(cliente.documento)
                )
        except Exception as error:
            self.__registrador.error(error, "registro de cliente '{0}'".format(nombre))
            raise
        else:
            self.__clientes.append(cliente)
            self.__registrador.evento(
                "Cliente registrado {0} - {1}".format(cliente.identificador, cliente.nombre)
            )
            return cliente
        finally:
            self.__registrador.evento(
                "Fin del intento de registro de cliente (total actual: {0})".format(
                    len(self.__clientes)
                )
            )

    def buscar_opcional(self, documento):
        texto = str(documento).strip()
        for cliente in self.__clientes:
            if cliente.documento == texto or cliente.identificador == texto:
                return cliente
        return None

    def buscar(self, documento):
        cliente = self.buscar_opcional(documento)
        if cliente is None:
            error = EntidadNoEncontradaError("No existe el cliente '{0}'".format(documento))
            self.__registrador.error(error, "busqueda de cliente")
            raise error
        return cliente

    def listar(self):
        return [cliente.resumen() for cliente in self.__clientes]
