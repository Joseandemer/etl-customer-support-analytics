
# Framework ETL (Código reutilizable)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FOLDER = os.path.join(BASE_DIR, "data")
RAW_FOLDER = os.path.join(DATA_FOLDER, "raw")
PROCESSED_FOLDER = os.path.join(DATA_FOLDER, "processed")
BACKUP_FOLDER = os.path.join(DATA_FOLDER, "backup")

LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# Personalizar según el dataset del proyecto.

SOURCE_FILE = "Customer_Support_Analytics_Dataset.xlsx"

SHEET_NAMES = [
    "tickets_raw",
    "agents_raw",
    "customers_raw",
    "surveys_raw"
]

RAW_FILE = os.path.join(RAW_FOLDER, SOURCE_FILE)

# Archivo de logs

LOG_FILE = os.path.join(LOG_FOLDER, "etl.log")
