"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioNoDisponibleError)
from logger import obtener_logger
from servicios import Servicio

log = obtener_logger()


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"

    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if not isinstance(cliente, Cliente):                 # valida tipos de los parámetros
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        servicio.validar_parametros(horas)                   # el propio servicio valida la duración
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE                        # estado inicial
        self._costo = None                                   # se calcula al procesar

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA (solo si el servicio está disponible)."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible.")
        self._estado = self.CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada."""
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}.")
        self._estado = self.CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")

    def procesar(self):
        """CONFIRMADA -> PROCESADA, calculando el costo. Usa try/except/else/finally."""
        try:
            if self._estado != self.CONFIRMADA:              # solo se procesa lo confirmado
                raise OperacionNoPermitidaError(f"No se puede procesar una reserva {self._estado}.")
            costo = self._servicio.calcular_costo(self._horas)
        except OperacionNoPermitidaError as e:
            log.error(f"Reserva #{self.id}: {e}")
            raise                                            # relanza la misma excepción
        except Exception as e:
            log.error(f"Reserva #{self.id}: fallo al calcular costo: {e}")
            # Encadenamiento de excepciones: conserva la causa original con "from e"
            raise CalculoInconsistenteError(f"No se pudo procesar la reserva #{self.id}.") from e
        else:                                                # solo si NO hubo errores
            self._costo = costo
            self._estado = self.PROCESADA
            log.info(f"Reserva #{self.id} procesada. Costo total: ${costo:,.2f}")
            return costo
        finally:                                             # se ejecuta siempre
            log.debug(f"Fin del intento de procesamiento de la reserva #{self.id}.")

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} -> {self._servicio.nombre} "
                f"| {self._horas} h | {self._estado} | Costo: {costo}")
