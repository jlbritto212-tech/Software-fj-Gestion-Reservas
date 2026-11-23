"""Simulación de 15 operaciones del sistema Software FJ (válidas e inválidas)."""
from gestor import GestorSoftwareFJ
from logger import obtener_logger
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

log = obtener_logger()


def titulo(numero, texto):
    """Imprime el encabezado de cada operación simulada."""
    print(f"\n--- Operación {numero}: {texto}")


def main():
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorSoftwareFJ()

    titulo(1, "Cliente válido (Ana)")
    ana = g.registrar_cliente("Ana Gómez", "1020304050", "ana@correo.com", "3001234567")

    titulo(2, "Cliente con correo inválido")
    g.registrar_cliente("Pedro Ruiz", "1098765432", "pedro-correo.com", "3109876543")

    titulo(3, "Cliente válido (Carlos)")
    carlos = g.registrar_cliente("Carlos Pérez", "80123456", "carlos@mail.com", "3205551234")

    titulo(4, "Cliente con documento no numérico y nombre None")
    g.registrar_cliente("Luisa Mora", "ABC123", "luisa@mail.com", "3001112233")
    g.registrar_cliente(None, "12345678", "x@mail.com", "3001112233")

    titulo(5, "Servicio válido: sala de reuniones")
    sala = g.crear_servicio(ReservaSala, "Sala Ejecutiva", 50000, 12)

    titulo(6, "Servicio válido: alquiler de equipo")
    equipo = g.crear_servicio(AlquilerEquipo, "Videobeam HD", 20000, "Proyector")

    titulo(7, "Servicio válido: asesoría (no disponible)")
    asesoria = g.crear_servicio(AsesoriaEspecializada, "Asesoría en Python", 80000, "senior", disponible=False)

    titulo(8, "Servicios inválidos: tarifa negativa, nivel inexistente y parámetro faltante")
    g.crear_servicio(ReservaSala, "Sala Rota", -100, 10)
    g.crear_servicio(AsesoriaEspecializada, "Asesoría X", 60000, "maestro")
    g.crear_servicio(AlquilerEquipo, "Portátil")  # faltan argumentos -> TypeError controlado

    titulo(9, "Reserva exitosa: Ana reserva la sala 3 h y se procesa")
    r1 = g.crear_reserva(ana, sala, 3)
    if r1:
        g.procesar_reserva(r1)

    titulo(10, "Reserva fallida: duración excesiva (50 h en una sala)")
    g.crear_reserva(carlos, sala, 50)

    titulo(11, "Reserva fallida: servicio no disponible (asesoría)")
    g.crear_reserva(carlos, asesoria, 2)

    titulo(12, "Cancelar una reserva ya procesada (operación no permitida)")
    if r1:
        g.cancelar_reserva(r1)

    titulo(13, "Reserva con cliente inexistente (None)")
    g.crear_reserva(None, equipo, 5)

    titulo(14, "Variantes de cálculo de costos (sobrecarga)")
    print(f"   Sala 4 h con IVA        : ${sala.calcular_costo(4):,.2f}")
    print(f"   Sala 4 h sin impuesto   : ${sala.calcular_costo(4, impuesto=0.0):,.2f}")
    print(f"   Sala 4 h con 10% desc.  : ${sala.calcular_costo(4, descuento=0.10):,.2f}")
    print(f"   Equipo 10 h (5% imp,10%): ${equipo.calcular_costo(10, 0.05, 0.10):,.2f}")
    try:
        sala.calcular_costo(4, descuento=0.9)  # descuento fuera de rango
    except Exception as e:
        log.error(f"Cálculo inválido: {e}")
        print(f"   [ERROR] {e}")

    titulo(15, "Reserva de equipo, confirmación y cancelación válida")
    r2 = g.crear_reserva(carlos, equipo, 6)
    if r2:
        g.cancelar_reserva(r2)
        g.procesar_reserva(r2)  # procesar una reserva cancelada -> error controlado

    print("\n===== RESUMEN =====")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print("  ", r.describir())
    print("\nEl programa terminó sin interrupciones. Revisa logs/software_fj.log")
    log.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    main()
