import math
from sqlalchemy import Column, Integer, Numeric, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

USER = "edielmi"
PASSWORD = "12345"
HOST = "localhost"
PORT = "5432"
DB_NAME = "cotizaciones"

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class CotizacionSexenio1824(Base):
  __tablename__ = "cotizaciones_sexenio_18_24"

  id = Column(Integer, primary_key=True)
  fecha = Column(String(50))
  determinacion = Column(String(50))
  publicacion_dof = Column(String(50))
  cotizacion = Column(Numeric(12, 10))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

registros = session.query(CotizacionSexenio1824).all()
session.close()

lista_cotizaciones = [
    float(reg.cotizacion) for reg in registros if reg.cotizacion is not None
]


def calcular_media_de(lista):
  n = len(lista)
  return sum(lista) / n if n > 0 else 0


def obtener_mediana_de(lista):
  n = len(lista)
  if n == 0:
    return 0
  lista_ordenada = sorted(lista)
  mitad = n // 2
  if n % 2 == 0:
    return (lista_ordenada[mitad - 1] + lista_ordenada[mitad]) / 2
  return lista_ordenada[mitad]


def obtener_minimo_de(lista):
  return min(lista) if lista else 0


def obtener_maximo_de(lista):
  return max(lista) if lista else 0


def obtener_rango_de(lista):
  return max(lista) - min(lista) if lista else 0


def obtener_desviacion_media_de(lista):
  n = len(lista)
  if n == 0:
    return 0
  media = calcular_media_de(lista)
  return sum(abs(x - media) for x in lista) / n


def obtener_varianza_de(lista, poblacional=False):
  n = len(lista)
  if n < 2 and not poblacional:
    return 0
  if n == 0:
    return 0
  media = calcular_media_de(lista)
  suma_cuadrados = sum((x - media) ** 2 for x in lista)
  return suma_cuadrados / (n if poblacional else n - 1)


def obtener_desviacion_estandar(lista, poblacional=False):
  return math.sqrt(obtener_varianza_de(lista, poblacional=poblacional))


media = calcular_media_de(lista_cotizaciones)
mediana = obtener_mediana_de(lista_cotizaciones)
minimo = obtener_minimo_de(lista_cotizaciones)
maximo = obtener_maximo_de(lista_cotizaciones)
rango = obtener_rango_de(lista_cotizaciones)
desv_media = obtener_desviacion_media_de(lista_cotizaciones)
varianza = obtener_varianza_de(lista_cotizaciones, poblacional=False)
desviacion = obtener_desviacion_estandar(lista_cotizaciones, poblacional=False)

print("\n-------------------------------------")
print("   RESULTADOS SEXENIO 2018-2024      ")
print("-------------------------------------")
print(f"Total de cotizaciones:   {len(lista_cotizaciones)}")
print(f"Media (Promedio):        {media:.4f} MXN")
print(f"Mediana:                 {mediana:.4f} MXN")
print(f"Desviación Estándar (σ): {desviacion:.4f}")
print(f"Varianza (s²):           {varianza:.4f}")
print(f"Desviación Media:        {desv_media:.4f} MXN")
print(f"Mínimo:                  {minimo:.4f} MXN")
print(f"Máximo:                  {maximo:.4f} MXN")
print(f"Rango (Máx - Mín):       {rango:.4f} MXN")
print("-------------------------------------\n")
