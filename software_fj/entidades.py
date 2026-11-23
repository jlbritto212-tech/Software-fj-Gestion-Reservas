"""Clase abstracta base del sistema y clase Cliente."""
import re                      # expresiones regulares para validar correo
from abc import ABC, abstractmethod  # soporte de clases abstractas
from itertools import count    # generador de números consecutivos para los IDs

from excepciones import ClienteInvalidoError
from logger import obtener_logger

log = obtener_logger()  # logger compartido del sistema


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    _contador = count(1)  # contador compartido para generar IDs únicos

    def __init__(self):
        self._id = next(EntidadBase._contador)  # asigna el siguiente ID disponible

    @property
    def id(self):
        """ID de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (método abstracto)."""


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()          # inicializa el ID de la entidad base
        self.nombre = nombre        # usa el setter con validación
        self.documento = documento  # usa el setter con validación
        self.correo = correo        # usa el setter con validación
        self.telefono = telefono    # usa el setter con validación

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):                      # debe ser texto
            raise ClienteInvalidoError("El nombre debe ser texto.")
        valor = valor.strip()                               # quita espacios sobrantes
        if len(valor) < 3 or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'.")
        self._nombre = valor                                # guarda el valor ya validado

    # ---------- documento ----------
    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip() if valor is not None else ""  # convierte a texto de forma segura
        if not re.fullmatch(r"\d{6,12}", valor):            # solo dígitos, entre 6 y 12
            raise ClienteInvalidoError(f"Documento inválido: '{valor}'.")
        self._documento = valor

    # ---------- correo ----------
    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip() if valor is not None else ""
        if not re.fullmatch(r"\d{7,10}", valor):            # entre 7 y 10 dígitos
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'.")
        self._telefono = valor

    def describir(self):
        """Implementación del método abstracto."""
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
