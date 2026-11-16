
# 📊 Customer Support Analytics - ETL con Python, SQL Server y Power BI

## Descripción

Proyecto de Data Analytics orientado al análisis de atención al cliente. Se desarrolló un pipeline ETL en Python para extraer, validar, limpiar y transformar datos de múltiples hojas de Excel, construir un modelo estrella en SQL Server y visualizar indicadores en Power BI.

## Tecnologías utilizadas

- Python y Pandas
- SQL Server
- Power BI y DAX
- Git y GitHub

## Flujo del proyecto

1. Extracción de datos desde cuatro fuentes de Excel.
2. Validación y limpieza de registros.
3. Transformación y estandarización de datos.
4. Construcción de dimensiones y tabla de hechos.
5. Carga de datos procesados a SQL Server.
6. Desarrollo de consultas SQL y medidas DAX.
7. Diseño de dashboard interactivo en Power BI.

## Modelo estrella

- `fact_tickets`
- `dim_agent`
- `dim_customer`
- `dim_category`
- `dim_channel`
- `dim_date`

![Modelo Estrella](docs/modelo_estrella.png)

## KPIs desarrollados

### Descriptivos
- Total de tickets registrados.
- Total de tickets resueltos.
- Total de tickets no resueltos.
- Promedio de tickets resueltos por cliente.
- Total de agentes registrados.

### Analíticos
- Evolución mensual de tickets resueltos.
- Tickets resueltos por canal de atención.
- Tickets resueltos por categoría de incidencia.
- Tickets resueltos por tipo de contacto.

## Dashboard

![Dashboard](docs/dashboard.png)

## Resultados principales

- 3,500 tickets registrados.
- 2,419 tickets resueltos.
- 1,081 tickets no resueltos.
- 42 agentes registrados.
- Tasa de resolución: 69.11%.
- Email es el canal con mayor cantidad de tickets resueltos.

## Conclusión

Se implementó un flujo completo de análisis de datos utilizando Python, SQL Server y Power BI, permitiendo evaluar el desempeño de la atención al cliente mediante indicadores operativos y visualizaciones interactivas.
