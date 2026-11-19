"""Punto de entrada del sistema Software FJ.

Arquitectura por capas:
    excepciones/      -> excepciones personalizadas
    infraestructura/  -> registro de eventos y errores en archivo de logs
    dominio/          -> entidades (abstractas y concretas) del negocio
    aplicacion/       -> gestores en memoria y simulacion de operaciones
    presentacion/     -> interfaz grafica en Tkinter
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infraestructura.registrador import Registrador  # noqa: E402
from presentacion.ventana_principal import VentanaPrincipal  # noqa: E402


def main():
    registrador = Registrador()
    try:
        ventana = VentanaPrincipal()
        ventana.mainloop()
    except Exception as error:
        registrador.error(error, "arranque de la aplicacion")
        print("Ocurrio un error al iniciar. Revise el archivo de logs:", registrador.ruta)
    finally:
        registrador.evento("Aplicacion finalizada")


if __name__ == "__main__":
    main()
