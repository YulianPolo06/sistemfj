"""Capa de aplicacion: catalogo de servicios en memoria."""

from dominio.alquiler_equipo import AlquilerEquipo
from dominio.asesoria import Asesoria
from dominio.sala_reuniones import SalaReuniones
from excepciones.errores import (
    DatosInvalidosError,
    EntidadNoEncontradaError,
    ParametroFaltanteError,
)


class GestorServicios:
    """Fabrica y almacena los tres tipos de servicio de Software FJ."""

    TIPOS = ("sala", "equipo", "asesoria")

    def __init__(self, registrador):
        self.__servicios = []
        self.__registrador = registrador

    @property
    def servicios(self):
        return tuple(self.__servicios)

    def crear(self, tipo, nombre, tarifa, parametro):
        clave = str(tipo).strip().lower() if tipo else ""
        try:
            if clave not in GestorServicios.TIPOS:
                raise DatosInvalidosError(
                    "Tipo de servicio '{0}' no soportado. Use: {1}".format(
                        tipo, ", ".join(GestorServicios.TIPOS)
                    )
                )
            if parametro is None or str(parametro).strip() == "":
                raise ParametroFaltanteError(
                    "Falta el parametro especifico del servicio '{0}'".format(clave)
                )

            if clave == "sala":
                servicio = SalaReuniones(nombre, tarifa, parametro)
            elif clave == "equipo":
                servicio = AlquilerEquipo(nombre, tarifa, parametro)
            else:
                servicio = Asesoria(nombre, tarifa, parametro)
        except Exception as error:
            self.__registrador.error(error, "creacion de servicio '{0}'".format(nombre))
            raise
        else:
            self.__servicios.append(servicio)
            self.__registrador.evento("Servicio creado {0}".format(servicio.resumen()))
            return servicio

    def buscar(self, identificador):
        texto = str(identificador).strip()
        for servicio in self.__servicios:
            if servicio.identificador == texto or servicio.nombre == texto:
                return servicio
        error = EntidadNoEncontradaError("No existe el servicio '{0}'".format(identificador))
        self.__registrador.error(error, "busqueda de servicio")
        raise error

    def cambiar_disponibilidad(self, identificador, disponible):
        servicio = self.buscar(identificador)
        if disponible:
            servicio.habilitar()
        else:
            servicio.inhabilitar()
        self.__registrador.evento(
            "Servicio {0} ahora esta {1}".format(
                servicio.identificador, "disponible" if disponible else "inhabilitado"
            )
        )
        return servicio

    def listar(self):
        return [servicio.resumen() for servicio in self.__servicios]
