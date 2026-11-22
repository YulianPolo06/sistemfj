"""Capa de presentacion: pestana de simulacion y visor de logs."""

import tkinter as tk
from tkinter import messagebox, ttk

from aplicacion.simulacion import Simulador


class PestanaSimulacion(ttk.Frame):
    def __init__(self, padre, gestor_clientes, gestor_servicios, gestor_reservas, registrador):
        super().__init__(padre, padding=10)
        self.__registrador = registrador
        self.__simulador = Simulador(
            gestor_clientes, gestor_servicios, gestor_reservas, registrador
        )
        self.__refrescar_otras = None
        self.__construir()

    def asignar_refresco_global(self, funcion):
        """Permite que la ventana principal actualice las demas pestanas."""
        self.__refrescar_otras = funcion

    def __construir(self):
        botones = ttk.Frame(self)
        botones.pack(fill="x")
        ttk.Button(
            botones, text="Ejecutar simulacion (14 operaciones)", command=self.__simular
        ).pack(side="left", padx=3)
        ttk.Button(botones, text="Ver archivo de logs", command=self.__ver_logs).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Limpiar logs", command=self.__limpiar_logs).pack(
            side="left", padx=3
        )

        ttk.Label(self, text="Archivo de logs: {0}".format(self.__registrador.ruta)).pack(
            anchor="w", pady=5
        )

        contenedor = ttk.LabelFrame(self, text="Resultados", padding=5)
        contenedor.pack(fill="both", expand=True)
        self.__texto = tk.Text(contenedor, height=20, wrap="word")
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=self.__texto.yview)
        self.__texto.configure(yscrollcommand=barra.set)
        self.__texto.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    def __mostrar(self, lineas):
        self.__texto.delete("1.0", tk.END)
        self.__texto.insert(tk.END, "\n".join(lineas))

    def __simular(self):
        try:
            resultados = self.__simulador.ejecutar()
        except Exception as error:  # la aplicacion no debe caer nunca
            self.__registrador.error(error, "ejecucion de la simulacion")
            messagebox.showerror("Error inesperado", str(error))
        else:
            self.__mostrar(resultados)
            if self.__refrescar_otras is not None:
                self.__refrescar_otras()

    def __ver_logs(self):
        self.__mostrar(self.__registrador.leer().splitlines())

    def __limpiar_logs(self):
        self.__registrador.limpiar()
        self.__registrador.evento("Archivo de logs reiniciado por el usuario")
        self.__ver_logs()

    def refrescar(self):
        return None
