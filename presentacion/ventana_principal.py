"""Capa de presentacion: ventana principal con pestanas."""

import tkinter as tk
from tkinter import messagebox, ttk

from aplicacion.gestor_clientes import GestorClientes
from aplicacion.gestor_reservas import GestorReservas
from aplicacion.gestor_servicios import GestorServicios
from infraestructura.registrador import Registrador
from presentacion.pestana_clientes import PestanaClientes
from presentacion.pestana_reservas import PestanaReservas
from presentacion.pestana_servicios import PestanaServicios
from presentacion.pestana_simulacion import PestanaSimulacion


class VentanaPrincipal(tk.Tk):
    """Compone las capas: infraestructura + aplicacion + presentacion."""

    def __init__(self):
        super().__init__()
        self.title("Software FJ - Gestion de Clientes, Servicios y Reservas")
        self.geometry("900x640")

        self.__registrador = Registrador()
        self.__gestor_clientes = GestorClientes(self.__registrador)
        self.__gestor_servicios = GestorServicios(self.__registrador)
        self.__gestor_reservas = GestorReservas(self.__registrador)

        self.__construir()
        self.__registrador.evento("Aplicacion iniciada")
        self.report_callback_exception = self.__error_no_controlado

    def __construir(self):
        ttk.Label(
            self, text="Software FJ", font=("Segoe UI", 16, "bold")
        ).pack(pady=8)

        self.__cuaderno = ttk.Notebook(self)
        self.__cuaderno.pack(fill="both", expand=True, padx=10, pady=5)

        self.__pestanas = [
            ("Clientes", PestanaClientes(self.__cuaderno, self.__gestor_clientes)),
            ("Servicios", PestanaServicios(self.__cuaderno, self.__gestor_servicios)),
            (
                "Reservas",
                PestanaReservas(
                    self.__cuaderno, self.__gestor_clientes,
                    self.__gestor_servicios, self.__gestor_reservas,
                ),
            ),
        ]
        simulacion = PestanaSimulacion(
            self.__cuaderno, self.__gestor_clientes, self.__gestor_servicios,
            self.__gestor_reservas, self.__registrador,
        )
        simulacion.asignar_refresco_global(self.refrescar_todo)
        self.__pestanas.append(("Simulacion y logs", simulacion))

        for titulo, pestana in self.__pestanas:
            self.__cuaderno.add(pestana, text=titulo)

        self.__cuaderno.bind("<<NotebookTabChanged>>", lambda evento: self.refrescar_todo())

    def refrescar_todo(self):
        for _, pestana in self.__pestanas:
            try:
                pestana.refrescar()
            except Exception as error:
                self.__registrador.error(error, "refresco de la interfaz")

    def __error_no_controlado(self, tipo, valor, traza):
        """Ultima red de seguridad: ningun error cierra la aplicacion."""
        self.__registrador.error(valor, "error no controlado en la interfaz")
        messagebox.showerror(
            "Error no controlado",
            "Se registro el error en el log y la aplicacion sigue activa:\n{0}".format(valor),
        )
