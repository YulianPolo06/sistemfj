"""Capa de presentacion: pestana de servicios."""

import tkinter as tk
from tkinter import messagebox, ttk

from excepciones.errores import ErrorSistemaFJ


class PestanaServicios(ttk.Frame):
    AYUDA = {
        "sala": "Capacidad (1 a 100 personas)",
        "equipo": "Cantidad de equipos",
        "asesoria": "Nivel: basico, intermedio o experto",
    }

    def __init__(self, padre, gestor_servicios):
        super().__init__(padre, padding=10)
        self.__gestor = gestor_servicios
        self.__tipo = tk.StringVar(value="sala")
        self.__construir()
        self.refrescar()

    def __construir(self):
        formulario = ttk.LabelFrame(self, text="Crear servicio", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Tipo de servicio").grid(row=0, column=0, sticky="w", pady=3)
        combo = ttk.Combobox(
            formulario, textvariable=self.__tipo, state="readonly",
            values=("sala", "equipo", "asesoria"), width=32,
        )
        combo.grid(row=0, column=1, pady=3, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda evento: self.__actualizar_ayuda())

        ttk.Label(formulario, text="Nombre").grid(row=1, column=0, sticky="w", pady=3)
        self.__nombre = ttk.Entry(formulario, width=35)
        self.__nombre.grid(row=1, column=1, pady=3, padx=5)

        ttk.Label(formulario, text="Tarifa base").grid(row=2, column=0, sticky="w", pady=3)
        self.__tarifa = ttk.Entry(formulario, width=35)
        self.__tarifa.grid(row=2, column=1, pady=3, padx=5)

        self.__etiqueta_param = ttk.Label(formulario, text=PestanaServicios.AYUDA["sala"])
        self.__etiqueta_param.grid(row=3, column=0, sticky="w", pady=3)
        self.__parametro = ttk.Entry(formulario, width=35)
        self.__parametro.grid(row=3, column=1, pady=3, padx=5)

        botones = ttk.Frame(formulario)
        botones.grid(row=4, column=1, sticky="e", pady=8)
        ttk.Button(botones, text="Crear", command=self.__crear).pack(side="left", padx=3)
        ttk.Button(
            botones, text="Habilitar", command=lambda: self.__disponibilidad(True)
        ).pack(side="left", padx=3)
        ttk.Button(
            botones, text="Inhabilitar", command=lambda: self.__disponibilidad(False)
        ).pack(side="left", padx=3)

        tabla = ttk.LabelFrame(self, text="Catalogo de servicios", padding=10)
        tabla.pack(fill="both", expand=True, pady=10)
        columnas = ("id", "tipo", "nombre", "tarifa", "unidad", "estado")
        self.__arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=9)
        for columna in columnas:
            self.__arbol.heading(columna, text=columna.capitalize())
            self.__arbol.column(columna, width=130, anchor="w")
        self.__arbol.pack(fill="both", expand=True)

    def __actualizar_ayuda(self):
        self.__etiqueta_param.config(text=PestanaServicios.AYUDA[self.__tipo.get()])

    def __crear(self):
        try:
            servicio = self.__gestor.crear(
                self.__tipo.get(), self.__nombre.get(),
                self.__tarifa.get(), self.__parametro.get(),
            )
        except ErrorSistemaFJ as error:
            messagebox.showerror(
                "Error controlado", "{0}: {1}".format(type(error).__name__, error)
            )
        else:
            messagebox.showinfo("Servicio creado", servicio.resumen())
            for entrada in (self.__nombre, self.__tarifa, self.__parametro):
                entrada.delete(0, tk.END)
        finally:
            self.refrescar()

    def __seleccionado(self):
        seleccion = self.__arbol.selection()
        if not seleccion:
            return None
        return self.__arbol.item(seleccion[0], "values")[0]

    def __disponibilidad(self, disponible):
        identificador = self.__seleccionado()
        if identificador is None:
            messagebox.showwarning("Sin seleccion", "Seleccione un servicio en la tabla")
            return
        try:
            self.__gestor.cambiar_disponibilidad(identificador, disponible)
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error controlado", str(error))
        finally:
            self.refrescar()

    def refrescar(self):
        for fila in self.__arbol.get_children():
            self.__arbol.delete(fila)
        for servicio in self.__gestor.servicios:
            self.__arbol.insert(
                "", "end",
                values=(
                    servicio.identificador, type(servicio).__name__, servicio.nombre,
                    "{0:,.0f}".format(servicio.tarifa_base), servicio.unidad_duracion(),
                    "Disponible" if servicio.disponible else "Inhabilitado",
                ),
            )
