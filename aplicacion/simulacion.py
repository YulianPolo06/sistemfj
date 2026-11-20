"""Simulacion de operaciones completas (validas e invalidas) del sistema."""

from excepciones.errores import ErrorSistemaFJ


class Simulador:
    """Ejecuta 14 operaciones demostrando que el sistema nunca se detiene."""

    def __init__(self, gestor_clientes, gestor_servicios, gestor_reservas, registrador):
        self.__clientes = gestor_clientes
        self.__servicios = gestor_servicios
        self.__reservas = gestor_reservas
        self.__registrador = registrador
        self.__salida = []

    def __intentar(self, titulo, funcion):
        """Ejecuta una operacion capturando cualquier error sin detener el flujo."""
        try:
            resultado = funcion()
        except ErrorSistemaFJ as error:
            self.__salida.append(
                "[ERROR CONTROLADO] {0} -> {1}: {2}".format(titulo, type(error).__name__, error)
            )
        except Exception as error:  # red de seguridad final
            self.__registrador.error(error, "simulacion: {0}".format(titulo))
            self.__salida.append(
                "[ERROR INESPERADO] {0} -> {1}: {2}".format(titulo, type(error).__name__, error)
            )
        else:
            self.__salida.append("[OK] {0} -> {1}".format(titulo, resultado))
        finally:
            self.__registrador.evento("Simulacion: operacion '{0}' finalizada".format(titulo))

    def ejecutar(self):
        self.__salida = []
        self.__registrador.evento("=== Inicio de la simulacion ===")

        # 1 y 2: clientes validos
        self.__intentar(
            "1. Registrar cliente valido",
            lambda: self.__clientes.registrar("Ana Gomez", "1098765", "ana@fj.com", "3001234567"),
        )
        self.__intentar(
            "2. Registrar cliente VIP",
            lambda: self.__clientes.registrar(
                "Luis Pardo", "2233445", "luis@fj.com", "3109876543", vip=True
            ),
        )
        # 3 y 4: clientes invalidos
        self.__intentar(
            "3. Registrar cliente con documento invalido",
            lambda: self.__clientes.registrar("Pedro Ruiz", "ABC123", "pedro@fj.com"),
        )
        self.__intentar(
            "4. Registrar cliente con correo invalido",
            lambda: self.__clientes.registrar("Marta Diaz", "5566778", "marta-fj.com"),
        )
        self.__intentar(
            "5. Registrar cliente duplicado",
            lambda: self.__clientes.registrar("Ana Gomez", "1098765", "ana2@fj.com"),
        )

        # 6 a 8: servicios validos
        self.__intentar(
            "6. Crear sala de reuniones",
            lambda: self.__servicios.crear("sala", "Sala Innovacion", 40000, 12),
        )
        self.__intentar(
            "7. Crear alquiler de equipos",
            lambda: self.__servicios.crear("equipo", "Portatiles Dell", 90000, 5),
        )
        self.__intentar(
            "8. Crear asesoria experta",
            lambda: self.__servicios.crear("asesoria", "Asesoria Cloud", 120000, "experto"),
        )
        # 9 y 10: servicios invalidos
        self.__intentar(
            "9. Crear servicio con tarifa invalida",
            lambda: self.__servicios.crear("sala", "Sala Economica", "gratis", 8),
        )
        self.__intentar(
            "10. Crear asesoria con nivel inexistente",
            lambda: self.__servicios.crear("asesoria", "Asesoria Legal", 80000, "maestro"),
        )

        # 11: reserva exitosa procesada
        self.__intentar("11. Reservar y procesar sala (4 horas)", self.__reserva_exitosa)
        # 12: reserva fallida por duracion
        self.__intentar("12. Reservar asesoria de 1 hora", self.__reserva_duracion_invalida)
        # 13: reserva sobre servicio inhabilitado
        self.__intentar("13. Reservar servicio inhabilitado", self.__reserva_no_disponible)
        # 14: operaciones no permitidas sobre una reserva cancelada
        self.__intentar("14. Procesar una reserva cancelada", self.__procesar_cancelada)

        self.__registrador.evento("=== Fin de la simulacion ===")
        self.__salida.append(
            "Total facturado en la simulacion: {0:,.2f}".format(
                self.__reservas.total_facturado()
            )
        )
        return list(self.__salida)

    # ------------------ operaciones compuestas ------------------
    def __reserva_exitosa(self):
        cliente = self.__clientes.buscar("1098765")
        servicio = self.__servicios.buscar("Sala Innovacion")
        reserva = self.__reservas.crear(cliente, servicio, 4)
        total = self.__reservas.procesar(reserva.identificador)
        return "{0} procesada por {1:,.2f}".format(reserva.identificador, total)

    def __reserva_duracion_invalida(self):
        cliente = self.__clientes.buscar("2233445")
        servicio = self.__servicios.buscar("Asesoria Cloud")
        reserva = self.__reservas.crear(cliente, servicio, 1)
        return reserva.identificador

    def __reserva_no_disponible(self):
        cliente = self.__clientes.buscar("2233445")
        servicio = self.__servicios.buscar("Portatiles Dell")
        self.__servicios.cambiar_disponibilidad(servicio.identificador, False)
        try:
            return self.__reservas.crear(cliente, servicio, 16).identificador
        finally:
            self.__servicios.cambiar_disponibilidad(servicio.identificador, True)

    def __procesar_cancelada(self):
        cliente = self.__clientes.buscar("2233445")
        servicio = self.__servicios.buscar("Portatiles Dell")
        reserva = self.__reservas.crear(cliente, servicio, 16)
        self.__reservas.cancelar(reserva.identificador, "prueba de estado invalido")
        return self.__reservas.procesar(reserva.identificador)
