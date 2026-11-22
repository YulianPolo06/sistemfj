"""Capa de presentacion: pestana de reservas."""

import tkinter as tk
from tkinter import messagebox, ttk

from excepciones.errores import ErrorSistemaFJ, ParametroFaltanteError


class PestanaReservas(ttk.Frame):
    def __init__(self, padre, gestor_clientes, gestor_servicios, gestor_reservas):
        super().__init__(padre, padding=10)
        self.__clientes = gestor_clientes
        self.__servicios = gestor_servicios
        self.__reservas = gestor_reservas
        self.__cliente_sel = tk.StringVar()
        self.__servicio_sel = tk.StringVar()
        self.__construir()
        self.refrescar()

    def __construir(self):
        formulario = ttk.LabelFrame(self, text="Nueva reserva", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Cliente").grid(row=0, column=0, sticky="w", pady=3)
        self.__combo_clientes = ttk.Combobox(
            formulario, textvariable=self.__cliente_sel, state="readonly", width=45
        )
        self.__combo_clientes.grid(row=0, column=1, pady=3, padx=5)

        ttk.Label(formulario, text="Servicio").grid(row=1, column=0, sticky="w", pady=3)
        self.__combo_servicios = ttk.Combobox(
            formulario, textvariable=self.__servicio_sel, state="readonly", width=45
        )
        self.__combo_servicios.grid(row=1, column=1, pady=3, padx=5)

        ttk.Label(formulario, text="Duracion (horas)").grid(row=2, column=0, sticky="w", pady=3)
        self.__duracion = ttk.Entry(formulario, width=48)
        self.__duracion.grid(row=2, column=1, pady=3, padx=5)

        ttk.Label(formulario, text="Descuento 0.0 - 0.5 (opcional)").grid(
            row=3, column=0, sticky="w", pady=3
        )
        self.__descuento = ttk.Entry(formulario, width=48)
        self.__descuento.grid(row=3, column=1, pady=3, padx=5)

        ttk.Label(formulario, text="Impuesto 0.0 - 0.5 (opcional)").grid(
            row=4, column=0, sticky="w", pady=3
        )
        self.__impuesto = ttk.Entry(formulario, width=48)
        self.__impuesto.grid(row=4, column=1, pady=3, padx=5)

        botones = ttk.Frame(formulario)
        botones.grid(row=5, column=1, sticky="e", pady=8)
        ttk.Button(botones, text="Crear y confirmar", command=self.__crear).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Procesar", command=self.__procesar).pack(side="left", padx=3)
        ttk.Button(botones, text="Cancelar", command=self.__cancelar).pack(side="left", padx=3)

        tabla = ttk.LabelFrame(
            self, text="Reservas (seleccione una para procesar o cancelar)", padding=10
        )
        tabla.pack(fill="both", expand=True, pady=10)
        columnas = ("id", "cliente", "servicio", "duracion", "estado", "costo")
        self.__arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=8)
        for columna in columnas:
            self.__arbol.heading(columna, text=columna.capitalize())
            self.__arbol.column(columna, width=130, anchor="w")
        self.__arbol.pack(fill="both", expand=True)

        self.__total = ttk.Label(self, text="Total facturado: 0.00")
        self.__total.pack(anchor="e")

    # ------------------ utilidades internas ------------------
    @staticmethod
    def __identificador(texto):
        if not texto:
            raise ParametroFaltanteError("Debe seleccionar un elemento de la lista")
        return texto.split(" - ")[0]

    def __seleccionada(self):
        seleccion = self.__arbol.selection()
        if not seleccion:
            raise ParametroFaltanteError("Seleccione una reserva en la tabla")
        return self.__arbol.item(seleccion[0], "values")[0]

    def __opcional(self, entrada):
        texto = entrada.get().strip()
        if texto == "":
            return None
        return texto

    # ------------------ acciones ------------------
    def __crear(self):
        try:
            cliente = self.__clientes.buscar(self.__identificador(self.__cliente_sel.get()))
            servicio = self.__servicios.buscar(self.__identificador(self.__servicio_sel.get()))
            reserva = self.__reservas.crear(cliente, servicio, self.__duracion.get())
        except ErrorSistemaFJ as error:
            messagebox.showerror(
                "Error controlado", "{0}: {1}".format(type(error).__name__, error)
            )
        else:
            messagebox.showinfo("Reserva creada", reserva.resumen())
            self.__duracion.delete(0, tk.END)
        finally:
            self.refrescar()

    def __procesar(self):
        try:
            identificador = self.__seleccionada()
            total = self.__reservas.procesar(
                identificador, self.__opcional(self.__descuento), self.__opcional(self.__impuesto)
            )
        except ErrorSistemaFJ as error:
            messagebox.showerror(
                "Error controlado", "{0}: {1}".format(type(error).__name__, error)
            )
        else:
            messagebox.showinfo("Reserva procesada", "Costo final: {0:,.2f}".format(total))
        finally:
            self.refrescar()

    def __cancelar(self):
        try:
            identificador = self.__seleccionada()
            self.__reservas.cancelar(identificador, "cancelada desde la interfaz")
        except ErrorSistemaFJ as error:
            messagebox.showerror(
                "Error controlado", "{0}: {1}".format(type(error).__name__, error)
            )
        else:
            messagebox.showinfo("Reserva cancelada", identificador)
        finally:
            self.refrescar()

    def refrescar(self):
        self.__combo_clientes["values"] = [
            "{0} - {1}".format(cliente.identificador, cliente.nombre)
            for cliente in self.__clientes.clientes
        ]
        self.__combo_servicios["values"] = [
            "{0} - {1}".format(servicio.identificador, servicio.nombre)
            for servicio in self.__servicios.servicios
        ]
        for fila in self.__arbol.get_children():
            self.__arbol.delete(fila)
        for reserva in self.__reservas.reservas:
            self.__arbol.insert(
                "", "end",
                values=(
                    reserva.identificador, reserva.cliente.nombre, reserva.servicio.nombre,
                    "{0:g} {1}(s)".format(reserva.duracion, reserva.servicio.unidad_duracion()),
                    reserva.estado, "{0:,.2f}".format(reserva.costo),
                ),
            )
        self.__total.config(
            text="Total facturado: {0:,.2f}".format(self.__reservas.total_facturado())
        )
