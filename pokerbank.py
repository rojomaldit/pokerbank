from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Jugador:
    nombre: str
    balance_final: float
    apuesta_inicial: float

    @property
    def deuda(self) -> float:
        """Calcula cuánto debe o le deben al jugador."""
        return self.balance_final - self.apuesta_inicial

def calcular_movimientos(jugadores: List[Jugador]) -> List[Tuple[str, str, float]]:
    """
    Calcula los movimientos mínimos necesarios para saldar las deudas.
    Retorna una lista de tuplas (pagador, receptor, monto).
    """
    # Crear diccionario de deudas
    deudas = {j.nombre: j.deuda for j in jugadores}
    
    # Verificar que la suma de deudas sea cercana a cero (considerando errores de punto flotante)
    if abs(sum(deudas.values())) > 0.01:
        raise ValueError("Error: La suma de deudas no es cero")
    
    # Separar deudores y acreedores
    deudores = [(nombre, deuda) for nombre, deuda in deudas.items() if deuda < 0]
    acreedores = [(nombre, deuda) for nombre, deuda in deudas.items() if deuda > 0]
    
    # Ordenar por monto absoluto de manera descendente
    deudores.sort(key=lambda x: x[1])  # Más negativo primero
    acreedores.sort(key=lambda x: x[1], reverse=True)  # Más positivo primero
    
    movimientos = []
    i_deudor = 0
    i_acreedor = 0
    
    # Mientras haya deudas por saldar
    while i_deudor < len(deudores) and i_acreedor < len(acreedores):
        deudor, deuda = deudores[i_deudor]
        acreedor, credito = acreedores[i_acreedor]
        
        # Tomar el menor valor absoluto entre la deuda y el crédito
        monto = min(-deuda, credito)
        
        # Registrar el movimiento
        movimientos.append((deudor, acreedor, monto))
        
        # Actualizar los saldos
        deudores[i_deudor] = (deudor, deuda + monto)
        acreedores[i_acreedor] = (acreedor, credito - monto)
        
        # Avanzar índices si la deuda o crédito se saldó completamente
        if abs(deuda + monto) < 0.01:
            i_deudor += 1
        if abs(credito - monto) < 0.01:
            i_acreedor += 1
    
    return movimientos

def generar_informe(movimientos: List[Tuple[str, str, float]]) -> str:
    """
    Genera un informe legible de los movimientos necesarios.
    """
    informe = ["Movimientos necesarios para saldar balances:"]
    for deudor, acreedor, monto in movimientos:
        informe.append(f"{deudor} le paga a {acreedor} ${monto:.2f}")
    return "\n".join(informe)

def main():
    # Ejemplo de uso
    jugadores = [
        Jugador("Juanpa", 111000, 25000-11.11),
        Jugador("Diego", 27200, 25000-11.11),
        Jugador("Agus", 77850, 25000-11.11),
        Jugador("Red", 0, 25000-11.11),
        Jugador("Chenzo", 0, 40000-11.11),
        Jugador("Nou", 17550, 25000-11.11),
        Jugador("Nico", 51800, 75000-11.11),
        Jugador("Facu", 54500, 50000-11.11),
        Jugador("Franco", 0, 50000-11.11),
    ]

    totalInvertido = 0
    balanceFinal = 0
    for j in jugadores:
        totalInvertido += j.apuesta_inicial
        balanceFinal += j.balance_final

    print("Total Invertido: ", totalInvertido)
    print("Total Deuda: ", balanceFinal)
    if balanceFinal - totalInvertido > 0.01:
        raise ValueError("Error: La suma de deudas no es cero")
    
    try:
        movimientos = calcular_movimientos(jugadores)
        print(generar_informe(movimientos))
    except ValueError as e:
        print(f"Error al calcular movimientos: {e}")

if __name__ == "__main__":
    main()