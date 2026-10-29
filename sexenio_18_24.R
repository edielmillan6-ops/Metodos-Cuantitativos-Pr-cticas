library(DBI)
library(RPostgres)

# 1. Conexión a PostgreSQL
usuario   <- "edielmi"
password  <- "12345"  # Tu contraseña de edielmi
host      <- "localhost"
port      <- 5432
db_nombre <- "examen"

con <- dbConnect(
  RPostgres::Postgres(),
  dbname   = db_nombre,
  host     = host,
  port     = port,
  user     = usuario,
  password = password
)

# 2. Consulta filtrando por el sexenio 2018-2024
query <- "SELECT fecha, precio FROM cotizacion_tmp 
          WHERE fecha BETWEEN '2018-12-01' AND '2024-09-30' 
            AND precio IS NOT NULL 
          ORDER BY fecha ASC;"

df <- dbGetQuery(con, query)
dbDisconnect(con)

# 3. Extraer valores numéricos
lista_cotizaciones <- as.numeric(df$precio)

# 4. Fórmulas
calcular_media_de <- function(lista) sum(lista) / length(lista)
obtener_mediana_de <- function(lista) {
  n <- length(lista)
  s <- sort(lista)
  m <- floor(n / 2)
  if (n %% 2 == 0) return((s[m] + s[m + 1]) / 2)
  return(s[m + 1])
}
obtener_varianza_de <- function(lista) sum((lista - calcular_media_de(lista))^2) / (length(lista) - 1)
obtener_desviacion_estandar <- function(lista) sqrt(obtener_varianza_de(lista))
obtener_desviacion_media_de <- function(lista) sum(abs(lista - calcular_media_de(lista))) / length(lista)

media       <- calcular_media_de(lista_cotizaciones)
mediana     <- obtener_mediana_de(lista_cotizaciones)
minimo      <- min(lista_cotizaciones)
maximo      <- max(lista_cotizaciones)
rango       <- maximo - minimo
desv_media  <- obtener_desviacion_media_de(lista_cotizaciones)
varianza    <- obtener_varianza_de(lista_cotizaciones)
desviacion  <- obtener_desviacion_estandar(lista_cotizaciones)

# 5. Imprimir resultados
cat("\n-------------------------------------\n")
cat("    RESULTADOS SEXENIO 2018-2024 (BD) \n")
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
