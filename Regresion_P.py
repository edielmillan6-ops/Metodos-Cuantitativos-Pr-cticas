x = [3, 4, 6, 4, 2, 5]
y = [6, 8, 9, 5, 4.5, 9.5]

# O puedes usar cualquiera de estos otros datasets descomentándolo:
# x = [5, 3, 7, 2, 8]
# y = [11, 6, 10, 6, 12]

# x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# y = [60, 65, 70, 75, 80, 85, 90, 95, 100, 105]

def media(x):
    return sum(x) / len(x)

def diferencia_cuadrado(x):
    la_media = media(x)
    la_diferencia = 0
    for i in x:
        la_diferencia = la_diferencia + (i - la_media) * (i - la_media)
    return la_diferencia

def diferencia_xy(x, y):
    mediax = media(x)
    mediay = media(y)
    lista_xy = [(a - mediax) * (b - mediay) for a, b in zip(x, y)]
    sumatoria = sum(lista_xy)
    return sumatoria

def obtener_b1(x, y):
    diferencia = diferencia_xy(x, y)
    diferencia_cuadrados = diferencia_cuadrado(x)
    return diferencia / diferencia_cuadrados

def obtener_b0(x, y):
    mediay = media(y)
    mediax = media(x)
    b1 = obtener_b1(x, y)
    return mediay - (b1 * mediax)

# Llamada a las funciones para ver los resultados en consola
print("Intercepto (b0):", obtener_b0(x, y))
print("Pendiente (b1):", obtener_b1(x, y))
