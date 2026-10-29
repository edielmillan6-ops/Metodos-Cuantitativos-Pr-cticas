def calcular_margen_contribucion(s: float, v: float) -> float:
    """Margen de Contribución Unitario (MCU = s - v)"""
    return s - v


def calcular_ratio_margen_contribucion(s: float, v: float) -> float:
    """Ratio de Margen de Contribución (Porcentaje sobre el precio)"""
    return (s - v) / s if s > 0 else 0.0


def calcular_ganancia(s: float, f: float, v: float, x: float) -> float:
    """Ganancia / Utilidad Total"""
    ingresos = s * x
    costos_totales = f + (v * x)
    return ingresos - costos_totales


def calcular_punto_equilibrio_unidades(s: float, f: float, v: float) -> float:
    """Punto de Equilibrio en Unidades (PE = f / (s - v))"""
    mcu = calcular_margen_contribucion(s, v)
    if mcu <= 0:
        raise ValueError(
            "El precio de venta (s) debe ser mayor al costo variable (v)."
        )
    return f / mcu


def calcular_punto_equilibrio_moneda(s: float, f: float, v: float) -> float:
    """Punto de Equilibrio en Dinero ($)"""
    pe_unidades = calcular_punto_equilibrio_unidades(s, f, v)
    return pe_unidades * s


def calcular_unidades_para_objetivo(
    s: float, f: float, v: float, ganancia_deseada: float
) -> float:
    """Unidades necesarias para alcanzar una ganancia objetivo"""
    mcu = calcular_margen_contribucion(s, v)
    if mcu <= 0:
        raise ValueError(
            "El precio de venta (s) debe ser mayor al costo variable (v)."
        )
    return (f + ganancia_deseada) / mcu


def calcular_margen_seguridad(
    s: float, f: float, v: float, x: float
) -> tuple[float, float]:
    """Margen de Seguridad en unidades y porcentaje (cuánto pueden caer las ventas antes de tener pérdidas)"""
    pe = calcular_punto_equilibrio_unidades(s, f, v)
    ms_unidades = x - pe
    ms_porcentaje = (ms_unidades / x) * 100 if x > 0 else 0.0
    return ms_unidades, ms_porcentaje


def solicitar_float(mensaje: str) -> float:
    """Función auxiliar para solicitar números flotantes de forma segura."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print(" Por favor ingresa un número positivo.")
                continue
            return valor
        except ValueError:
            print(" Entrada inválida. Ingresa un número válido.")


def menu_interactivo():
    print("=" * 45)
    print("      ANÁLISIS COSTO-VOLUMEN-UTILIDAD")
    print("=" * 45)

    s = solicitar_float("Ingresa el Precio de Venta por unidad (s): ")
    f = solicitar_float("Ingresa el Costo Fijo total (f): ")
    v = solicitar_float("Ingresa el Costo Variable por unidad (v): ")
    x = solicitar_float("Ingresa el Número de Unidades Vendidas (X): ")

    mcu = calcular_margen_contribucion(s, v)
    ratio_mc = calcular_ratio_margen_contribucion(s, v)
    ganancia = calcular_ganancia(s, f, v, x)

    print("\n" + "-" * 45)
    print("RESULTADOS PRINCIPALES:")
    print("-" * 45)
    print(f"Margen de Contribución Unitario: ${mcu:,.2f}")
    print(f"Ratio Margen de Contribución:    {ratio_mc * 100:.2f}%")
    print(f"Ganancia Total Actual:           ${ganancia:,.2f}")

    if s > v:
        pe_u = calcular_punto_equilibrio_unidades(s, f, v)
        pe_m = calcular_punto_equilibrio_moneda(s, f, v)
        ms_u, ms_p = calcular_margen_seguridad(s, f, v, x)

        print(f"Punto de Equilibrio (Unidades): {pe_u:,.2f} unidades")
        print(f"Punto de Equilibrio (Dinero):   ${pe_m:,.2f}")
        print(f"Margen de Seguridad:             {ms_u:,.2f} unidades ({ms_p:.2f}%)")
    else:
        print("\n El costo variable supera o iguala al precio de venta; no hay punto de equilibrio.")

    # Opción adicional: Proyección de ganancia deseada
    print("\n" + "-" * 45)
    desea_objetivo = input("¿Deseas calcular unidades para una ganancia objetivo? (s/n): ").strip().lower()
    if desea_objetivo == 's' and s > v:
        g_deseada = solicitar_float("Ingresa la Ganancia Objetivo deseada ($): ")
        u_req = calcular_unidades_para_objetivo(s, f, v, g_deseada)
        print(f"-> Necesitas vender {u_req:,.2f} unidades para ganar ${g_deseada:,.2f}")


if __name__ == "__main__":
    menu_interactivo()