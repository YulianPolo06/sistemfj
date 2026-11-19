"""Entidad Cliente con encapsulacion y validaciones robustas."""

import re

from dominio.entidad_base import EntidadBase
from excepciones.errores import DatosInvalidosError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos personales estan encapsulados."""

    PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")

    def __init__(self, nombre, documento, correo, telefono="", vip=False):
        super().__init__(prefijo="CLI")
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.__vip = bool(vip)
        self.__reservas = []  # lista interna de reservas del cliente

    # ------------------ propiedades encapsuladas ------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre del cliente es obligatorio")
        texto = str(valor).strip()
        if len(texto) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres")
        if any(caracter.isdigit() for caracter in texto):
            raise DatosInvalidosError("El nombre no puede contener numeros")
        self.__nombre = texto

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El documento es obligatorio")
        texto = str(valor).strip()
        if not texto.isdigit():
            raise DatosInvalidosError("El documento solo admite digitos")
        if not 5 <= len(texto) <= 12:
            raise DatosInvalidosError("El documento debe tener entre 5 y 12 digitos")
        self.__documento = texto

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo es obligatorio")
        texto = str(valor).strip()
        if not Cliente.PATRON_CORREO.match(texto):
            raise DatosInvalidosError("El correo '{0}' no tiene un formato valido".format(texto))
        self.__correo = texto

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = "" if valor is None else str(valor).strip()
        if texto and (not texto.isdigit() or len(texto) < 7):
            raise DatosInvalidosError("El telefono debe tener al menos 7 digitos")
        self.__telefono = texto

    @property
    def vip(self):
        return self.__vip

    @property
    def reservas(self):
        return tuple(self.__reservas)  # copia inmutable: protege la lista interna

    # ------------------ comportamiento ------------------
    def agregar_reserva(self, reserva):
        self.__reservas.append(reserva)

    def descuento_aplicable(self):
        """Clientes VIP o con historial obtienen descuento."""
        if self.__vip:
            return 0.15
        if len(self.__reservas) >= 3:
            return 0.05
        return 0.0

    def descripcion(self):
        etiqueta = "VIP" if self.__vip else "estandar"
        return "Cliente {0} (doc. {1}, {2}, {3}) reservas: {4}".format(
            self.nombre, self.documento, self.correo, etiqueta, len(self.__reservas)
        )

    def validar(self):
        # Reasignar fuerza nuevamente las validaciones de los setters.
        self.nombre = self.__nombre
        self.documento = self.__documento
        self.correo = self.__correo
        return True
