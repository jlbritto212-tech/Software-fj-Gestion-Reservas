"""Gestor del sistema: administra listas internas y captura errores para que el programa no se detenga."""
from entidades import Cliente
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ, ServicioInvalidoError
from logger import obtener_logger
from reserva import Reserva

log = obtener_logger()


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en listas (sin base de datos)."""

    def __init__(self):
        self.clientes = []    # lista interna de clientes
        self.servicios = []   # lista interna de servicios
        self.reservas = []    # lista interna de reservas

    def registrar_cliente(self, nombre, documento, correo, telefono):
        """Crea y guarda un cliente. Devuelve el cliente o None si hubo error."""
        try:
            cliente = Cliente(nombre, documento, correo, telefono)
        except ClienteInvalidoError as e:                    # error esperado de validación
            log.error(f"Registro de cliente fallido: {e}")
            print(f"   [ERROR] Cliente no registrado: {e}")
            return None
        except Exception as e:                               # cualquier error inesperado
            log.critical(f"Error inesperado registrando cliente: {e!r}")
            print(f"   [ERROR INESPERADO] {e!r}")
            return None
        else:                                                # solo si todo salió bien
            self.clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.describir()}")
            print(f"   [OK] {cliente.describir()}")
            return cliente

    def crear_servicio(self, clase_servicio, *args, **kwargs):
        """Crea un servicio de cualquier tipo (polimorfismo). Devuelve el servicio o None."""
        try:
            servicio = clase_servicio(*args, **kwargs)
        except ErrorSoftwareFJ as e:
            log.error(f"Creación de servicio fallida ({clase_servicio.__name__}): {e}")
            print(f"   [ERROR] Servicio no creado: {e}")
            return None
        except TypeError as e:                               # faltan o sobran argumentos
            log.error(f"Parámetros incorrectos para {clase_servicio.__name__}: {e}")
            print(f"   [ERROR] Parámetros incorrectos: {e}")
            return None
        else:
            self.servicios.append(servicio)
            log.info(f"Servicio creado: {servicio.describir()}")
            print(f"   [OK] {servicio.describir()}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas):
        """Crea y confirma una reserva. Devuelve la reserva o None si falla."""
        try:
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()
        except ErrorSoftwareFJ as e:
            log.error(f"Reserva fallida: {e}")
            print(f"   [ERROR] Reserva no realizada: {e}")
            return None
        else:
            self.reservas.append(reserva)
            print(f"   [OK] {reserva.describir()}")
            return reserva
        finally:
            log.debug("Intento de creación de reserva finalizado.")

    def procesar_reserva(self, reserva):
        """Procesa una reserva capturando cualquier error y mostrando la causa encadenada."""
        try:
            costo = reserva.procesar()
        except ErrorSoftwareFJ as e:
            causa = f" (causa: {e.__cause__})" if e.__cause__ else ""  # muestra el encadenamiento
            print(f"   [ERROR] No se pudo procesar: {e}{causa}")
            return None
        print(f"   [OK] Reserva #{reserva.id} procesada. Total: ${costo:,.2f}")
        return costo

    def cancelar_reserva(self, reserva):
        """Cancela una reserva capturando operaciones no permitidas."""
        try:
            reserva.cancelar()
        except ErrorSoftwareFJ as e:
            log.error(f"Cancelación fallida: {e}")
            print(f"   [ERROR] No se pudo cancelar: {e}")
            return False
        print(f"   [OK] Reserva #{reserva.id} cancelada.")
        return True
