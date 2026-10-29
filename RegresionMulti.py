import pandas as pd
import statsmodels.formula.api as smf

def crear_datos() -> pd.DataFrame:
    """
    Crea y retorna un DataFrame con los datos de las 14 casas 
    del caso Jenny Wilson Realty (precio, pies cuadrados, antigüedad y condición).
    
    Retorna:
    --------
    pd.DataFrame
        Marco de datos con la información de las casas.
    """
    precio = [
        95000, 119000, 124800, 135000, 142800, 145000, 159000,
        165000, 182000, 183000, 200000, 211000, 215000, 219000
    ]
    
    pies_cuadrados = [
        1926, 2069, 1720, 1396, 1706, 1847, 1950,
        2323, 2285, 3752, 2300, 2525, 3800, 1740
    ]
    
    antiguedad = [
        30, 40, 30, 15, 32, 38, 27,
        30, 26, 35, 18, 17, 40, 12
    ]
    
    condicion = [
        "Buena", "Excelente", "Excelente", "Buena",
        "Nueva", "Nueva", "Nueva", "Excelente",
        "Nueva", "Buena", "Buena", "Buena",
        "Excelente", "Nueva"
    ]
    
    return pd.DataFrame({
        'precio': precio,
        'pies_cuadrados': pies_cuadrados,
        'antiguedad': antiguedad,
        'condicion': condicion
    })

def ajustar_modelo(datos_casas: pd.DataFrame):
    """
    Ajusta un modelo de regresión lineal múltiple utilizando Mínimos Cuadrados Ordinarios (OLS).
    La variable dependiente es 'precio' y las independientes son 'pies_cuadrados' y 'antiguedad'.
    
    Parámetros:
    -----------
    datos_casas : pd.DataFrame
        DataFrame que contiene las variables del modelo.
        
    Retorna:
    --------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        El objeto con el modelo de regresión ajustado.
    """
    modelo_multi = smf.ols(
        'precio ~ pies_cuadrados + antiguedad', 
        data=datos_casas
    ).fit()
    
    return modelo_multi

def mostrar_resumen(modelo):
    """
    Muestra en consola el resumen estadístico completo y los coeficientes del modelo.
    
    Parámetros:
    -----------
    modelo : statsmodels.regression.linear_model.RegressionResultsWrapper
        El modelo de regresión ajustado.
    """
    print("\nRESUMEN ESTADISTICO\n")
    print(modelo.summary())
    
    print("\nCOEFICIENTES DEL MODELO\n")
    print(modelo.params)

def pronosticar_precio(modelo, pies_cuadrados: float, antiguedad: float) -> float:
    """
    Pronostica el precio estimado de una casa dados sus pies cuadrados y su antigüedad.
    
    Parámetros:
    -----------
    modelo : statsmodels.regression.linear_model.RegressionResultsWrapper
        El modelo de regresión ajustado.
    pies_cuadrados : float
        Superficie de la casa en pies cuadrados.
    antiguedad : float
        Antigüedad de la casa en años.
        
    Retorna:
    --------
    float
        El precio estimado en dólares.
    """
    nueva_casa = pd.DataFrame({
        'pies_cuadrados': [pies_cuadrados],
        'antiguedad': [antiguedad]
    })
    
    precio_estimado = modelo.predict(nueva_casa)
    return precio_estimado.iloc[0]

if __name__ == "__main__":
    datos_casas = crear_datos()
    print("\nDATOS DE LAS CASAS\n")
    print(datos_casas)

    modelo_multi = ajustar_modelo(datos_casas)
    mostrar_resumen(modelo_multi)

    precio_est = pronosticar_precio(modelo_multi, pies_cuadrados=2000, antiguedad=10)
    
    print("\nDATOS DE LA CASA A PRONOSTICAR")
    print("Pies cuadrados: 2000 | Antigüedad: 10 años")
    print(f"\nPrecio estimado: {precio_est:.2f} dolares\n")
