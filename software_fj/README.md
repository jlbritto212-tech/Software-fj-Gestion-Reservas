# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto en Python (POO + manejo avanzado de excepciones), sin bases de datos.

## Estructura
- `excepciones.py`: excepciones personalizadas (jerarquía desde `ErrorSoftwareFJ`).
- `logger.py`: configuración del archivo de logs (`logs/software_fj.log`).
- `entidades.py`: clase abstracta `EntidadBase` y clase `Cliente`.
- `servicios.py`: clase abstracta `Servicio` + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`.
- `reserva.py`: clase `Reserva` (confirmar, cancelar, procesar).
- `gestor.py`: listas internas y captura de errores.
- `main.py`: simulación de 15 operaciones válidas e inválidas.

## Ejecución
```
python main.py
```
Requiere Python 3.8 o superior. No usa librerías externas.
