"""Capa de presentacion: pestana de clientes."""

import tkinter as tk
from tkinter import messagebox, ttk

from excepciones.errores import ErrorSistemaFJ


class PestanaClientes(ttk.Frame):
    def __init__(self, padre, gestor_clientes):
        super().__init__(padre, padding=10)
        self.__gestor = gestor_clientes
        self.__campos = {}
        self.__vip = tk.BooleanVar(value=False)
        self.__construir()
        self.refrescar()

    def __construir(self):
        formulario = ttk.LabelFrame(self, text="Registrar cliente", padding=10)
        formulario.pack(fill="x")

        etiquetas = [
            ("nombre", "Nombre completo"),
            ("documento", "Documento (solo digitos)"),
            ("correo", "Correo electronico"),
            ("telefono", "Telefono (opcional)"),
        ]
        for fila, (clave, titulo) in enumerate(etiquetas):
            ttk.Label(formulario, text=titulo).grid(row=fila, column=0, sticky="w", pady=3)
            entrada = ttk.Entry(formulario, width=35)
            entrada.grid(row=fila, column=1, pady=3, padx=5)
            self.__campos[clave] = entrada

        ttk.Checkbutton(formulario, text="Cliente VIP", variable=self.__vip).grid(
            row=len(etiquetas), column=1, sticky="w"
        )
        ttk.Button(formulario, text="Registrar", command=self.__registrar).grid(
            row=len(etiquetas) + 1, column=1, sticky="e", pady=8
        )

        tabla = ttk.LabelFrame(self, text="Clientes registrados", padding=10)
        tabla.pack(fill="both", expand=True, pady=10)
        columnas = ("id", "nombre", "documento", "correo", "tipo", "reservas")
        self.__arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=9)
        for columna in columnas:
            self.__arbol.heading(columna, text=columna.capitalize())
            self.__arbol.column(columna, width=130, anchor="w")
        self.__arbol.pack(fill="both", expand=True)

    def __registrar(self):
        datos = {clave: entrada.get() for clave, entrada in self.__campos.items()}
        try:
            cliente = self.__gestor.registrar(
                datos["nombre"], datos["documento"], datos["correo"],
                datos["telefono"], self.__vip.get(),
            )
        except ErrorSistemaFJ as error:
            messagebox.showerror(
                "Error controlado", "{0}: {1}".format(type(error).__name__, error)
            )
        else:
            messagebox.showinfo("Cliente registrado", cliente.resumen())
            for entrada in self.__campos.values():
                entrada.delete(0, tk.END)
            self.__vip.set(False)
        finally:
            self.refrescar()

    def refrescar(self):
        for fila in self.__arbol.get_children():
            self.__arbol.delete(fila)
        for cliente in self.__gestor.clientes:
            self.__arbol.insert(
                "", "end",
                values=(
                    cliente.identificador, cliente.nombre, cliente.documento,
                    cliente.correo, "VIP" if cliente.vip else "Estandar",
                    len(cliente.reservas),
                ),
            )
