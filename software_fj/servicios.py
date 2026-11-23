"""Clase abstracta Servicio y tres servicios especializados (herencia y polimorfismo)."""
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)


class Servicio(EntidadBase, ABC):
    """Clase abstracta para todos los servicios que ofrece Software FJ."""

    IVA = 0.19  # impuesto por defecto (19 %)

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():       # nombre obligatorio
            raise ServicioInvalidoError("El servicio requiere un nombre válido.")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}.")
        self._nombre = nombre.strip()       # atributos protegidos (encapsulación)
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    # ---------- propiedades de solo lectura / controladas ----------
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # ---------- métodos abstractos (cada servicio los sobrescribe) ----------
    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parámetros de uso del servicio."""

    @abstractmethod
    def calcular_costo_base(self, horas):
        """Costo sin impuestos ni descuentos."""

    # ---------- método sobrecargado (variantes mediante parámetros opcionales) ----------
    def calcular_costo(self, horas, impuesto=None, descuento=0.0):
        """
        Variantes de uso (sobrecarga simulada con parámetros opcionales):
          calcular_costo(horas)                      -> con IVA por defecto
          calcular_costo(horas, impuesto=0.0)        -> sin impuesto
          calcular_costo(horas, descuento=0.10)      -> con IVA y 10 % de descuento
          calcular_costo(horas, 0.05, 0.10)          -> impuesto y descuento personalizados
        """
        self.validar_parametros(horas)                       # valida antes de calcular
        impuesto = self.IVA if impuesto is None else impuesto  # usa IVA si no se indicó
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 0.5):
            raise ServicioInvalidoError(f"Impuesto ({impuesto}) o descuento ({descuento}) fuera de rango.")
        base = self.calcular_costo_base(horas)               # costo base (polimórfico)
        total = base * (1 - descuento) * (1 + impuesto)      # aplica descuento e impuesto
        if total < 0:                                        # cálculo inconsistente
            raise CalculoInconsistenteError(f"Costo negativo calculado para {self.nombre}.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        if horas is None:
            raise ParametroFaltanteError("Falta indicar las horas de la sala.")
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 12):
            raise ServicioInvalidoError(f"Horas inválidas para sala (1-12): {horas!r}.")

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas

    def describir(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"Sala '{self.nombre}' (cap. {self._capacidad}) - ${self.tarifa_hora:,.0f}/h - {estado}"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (incluye cargo fijo de seguro)."""

    SEGURO = 0.05  # 5 % del valor base

    def __init__(self, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El equipo requiere un tipo válido.")
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas):
        if horas is None:
            raise ParametroFaltanteError("Falta indicar las horas de alquiler.")
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 72):
            raise ServicioInvalidoError(f"Horas inválidas para equipo (1-72): {horas!r}.")

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas * (1 + self.SEGURO)  # suma el seguro

    def describir(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"Equipo '{self.nombre}' ({self._tipo_equipo}) - ${self.tarifa_hora:,.0f}/h + seguro - {estado}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías; el nivel del asesor modifica la tarifa."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # multiplicadores de tarifa

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}. Opciones: {list(self.NIVELES)}.")
        self._nivel = nivel.lower()

    def validar_parametros(self, horas):
        if horas is None:
            raise ParametroFaltanteError("Falta indicar las horas de asesoría.")
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 8):
            raise ServicioInvalidoError(f"Horas inválidas para asesoría (1-8): {horas!r}.")

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"Asesoría '{self.nombre}' (nivel {self._nivel}) - ${self.tarifa_hora:,.0f}/h - {estado}"
