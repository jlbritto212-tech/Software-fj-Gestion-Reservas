"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente son inválidos o el cliente no existe."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio se crea o se usa con datos inválidos."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de una reserva son incorrectos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación no válida para el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inconsistente."""
