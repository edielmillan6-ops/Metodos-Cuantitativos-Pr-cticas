# Cargar librerías necesarias
library(DBI)
library(RPostgres)

# 1. Configuración de conexión a PostgreSQL
usuario   <- "edielmi"
password  <- "12345"  # Reemplaza con tu contraseña de edielmi
host      <- "localhost"
port      <- 5432
db_nombre <- "examen"

# 2. Conexión a la base de datos
con <- dbConnect(
  RPostgres::Postgres(),
  dbname   = db_nombre,
  host     = host,
  port     = port,
  user     = usuario,
  password = password
)

# 3. Consulta de los registros limpios ordenados por fecha
query <- "SELECT id, fecha, precio FROM cotizacion_tmp WHERE precio IS NOT NULL ORDER BY fecha ASC;"
df <- dbGetQuery(con, query)

# Cerrar la conexión
dbDisconnect(con)

# 4. Extraer el vector numérico de cotizaciones
lista_cotizaciones <- as.numeric(df$precio)

# 5. Funciones estadísticas implementadas paso a paso
calcular_media_de <- function(lista) {
  n <- length(lista)
  if (n == 0) return(0)
  return(sum(lista) / n)
}

obtener_mediana_de <- function(lista) {
  n <- length(lista)
  if (n == 0) return(0)
  lista_ordenada <- sort(lista)
  mitad <- floor(n / 2)
  if (n %% 2 == 0) {
    return((lista_ordenada[mitad] + lista_ordenada[mitad + 1]) / 2)
  }
  return(lista_ordenada[mitad + 1])
}

obtener_minimo_de <- function(lista) {
  if (length(lista) == 0) return(0)
  return(min(lista))
}

obtener_maximo_de <- function(lista) {
  if (length(lista) == 0) return(0)
  return(max(lista))
}

obtener_rango_de <- function(lista) {
  if (length(lista) == 0) return(0)
  return(max(lista) - min(lista))
}

obtener_desviacion_media_de <- function(lista) {
  n <- length(lista)
  if (n == 0) return(0)
  media <- calcular_media_de(lista)
  return(sum(abs(lista - media)) / n)
}

obtener_varianza_de <- function(lista, poblacional = FALSE) {
  n <- length(lista)
  if (n < 2 && !poblacional) return(0)
  if (n == 0) return(0)
  media <- calcular_media_de(lista)
  suma_cuadrados <- sum((lista - media)^2)
  denominador <- if (poblacional) n else (n - 1)
  return(suma_cuadrados / denominador)
}

obtener_desviacion_estandar <- function(lista, poblacional = FALSE) {
  return(sqrt(obtener_varianza_de(lista, poblacional = poblacional)))
}

# 6. Cálculo de métricas
media       <- calcular_media_de(lista_cotizaciones)
mediana     <- obtener_mediana_de(lista_cotizaciones)
minimo      <- obtener_minimo_de(lista_cotizaciones)
maximo      <- obtener_maximo_de(lista_cotizaciones)
rango       <- obtener_rango_de(lista_cotizaciones)
desv_media  <- obtener_desviacion_media_de(lista_cotizaciones)
varianza    <- obtener_varianza_de(lista_cotizaciones, poblacional = FALSE)
desviacion  <- obtener_desviacion_estandar(lista_cotizaciones, poblacional = FALSE)

# 7. Imprimir resultados formateados
cat("\n-------------------------------------\n")
cat("    RESULTADOS SEXENIO 2012-2018 (R) \n")
cat("-------------------------------------\n")
cat(sprintf("Total de cotizaciones:   %d\n", length(lista_cotizaciones)))
cat(sprintf("Media (Promedio):        %.4f MXN\n", media))
cat(sprintf("Mediana:                 %.4f MXN\n", mediana))
cat(sprintf("Desviación Estándar (s): %.4f\n", desviacion))
cat(sprintf("Varianza (s²):           %.4f\n", varianza))
cat(sprintf("Desviación Media:        %.4f MXN\n", desv_media))
cat(sprintf("Mínimo:                  %.4f MXN\n", minimo))
cat(sprintf("Máximo:                  %.4f MXN\n", maximo))
cat(sprintf("Rango (Máx - Mín):       %.4f MXN\n", rango))
cat("-------------------------------------\n\n")
