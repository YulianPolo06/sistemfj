# Software FJ — Sistema de Gestión de Clientes, Servicios y Reservas

Aplicación de escritorio en **Python + Tkinter**, orientada a objetos, **sin base de datos**
(todo se maneja en objetos y listas en memoria; el archivo sólo se usa para los *logs*).

## Ejecución

```bash
python main.py
```

Requiere Python 3.8+ con Tkinter (incluido en la instalación estándar de Windows).

## Arquitectura por capas

| Capa | Carpeta | Contenido |
|------|---------|-----------|
| Excepciones | `excepciones/` | `errores.py`: excepciones personalizadas (`ErrorSistemaFJ` y 8 derivadas) |
| Infraestructura | `infraestructura/` | `registrador.py`: escritura de eventos/errores en `logs/sistema.log` |
| Dominio | `dominio/` | Una clase por archivo: `entidad_base.py`, `cliente.py`, `servicio.py`, `sala_reuniones.py`, `alquiler_equipo.py`, `asesoria.py`, `reserva.py` |
| Aplicación | `aplicacion/` | `gestor_clientes.py`, `gestor_servicios.py`, `gestor_reservas.py`, `simulacion.py` |
| Presentación | `presentacion/` | `ventana_principal.py` y una pestaña por archivo: clientes, servicios, reservas, simulación/logs |

## Requisitos del ejercicio y dónde se cumplen

- **Clase abstracta general**: `EntidadBase` (`dominio/entidad_base.py`) con métodos abstractos
  `descripcion()` y `validar()`; de ella heredan `Cliente`, `Servicio` y `Reserva`.
- **Encapsulación**: atributos privados (`__nombre`, `__documento`, …) expuestos con
  `@property` y validados en los *setters*; las listas internas se devuelven como tuplas.
- **Clase abstracta `Servicio`** + **3 servicios especializados** con métodos sobrescritos
  (`calcular_costo`, `validar_parametros`, `unidad_duracion`, `descripcion`):
  - `SalaReuniones`: cobro por hora, recargo del 20 % si la capacidad supera 10 personas.
  - `AlquilerEquipo`: cobro por día (convierte horas a días, jornada de 8 h).
  - `Asesoria`: cobro por hora con multiplicador por nivel y mínimo de 2 horas.
- **Polimorfismo**: la misma llamada `servicio.calcular_costo_total(...)` produce cálculos
  distintos según el tipo real del servicio.
- **Método sobrecargado**: `Servicio.calcular_costo_total(*args, **kwargs)` admite
  `(duración)`, `(duración, descuento)`, `(duración, descuento, impuesto)` y la forma con
  parámetros por nombre.
- **Clase `Reserva`**: integra cliente, servicio, duración y estado
  (`PENDIENTE → CONFIRMADA → PROCESADA | CANCELADA`) con `confirmar()`, `cancelar()` y
  `procesar()`.
- **Manejo avanzado de excepciones**: `try/except`, `try/except/else`, `try/except/finally`
  y encadenamiento con `raise ... from error` (por ejemplo en `Servicio.tarifa_base` y
  `Reserva.procesar`). La ventana principal además sobrescribe
  `report_callback_exception` como última red de seguridad: ningún error cierra la app.
- **Archivo de logs**: `logs/sistema.log`, visible y administrable desde la pestaña
  *Simulación y logs*.
- **Simulación de operaciones**: `aplicacion/simulacion.py` ejecuta **14 operaciones**
  (clientes válidos/inválidos, servicios válidos/inválidos, reservas exitosas y fallidas)
  y muestra el resultado de cada una sin detener la aplicación.

## Uso de la interfaz

1. **Clientes**: registra clientes (los datos inválidos muestran el error y quedan en el log).
2. **Servicios**: crea salas, alquileres o asesorías; selecciona una fila para
   habilitar/inhabilitar el servicio.
3. **Reservas**: elige cliente y servicio, indica la duración y pulsa *Crear y confirmar*;
   luego selecciona la reserva y pulsa *Procesar* (descuento e impuesto son opcionales) o
   *Cancelar*.
4. **Simulación y logs**: ejecuta las 14 operaciones de prueba y permite ver o limpiar el
   archivo de logs.
