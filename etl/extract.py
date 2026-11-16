
# Framework ETL (Código reutilizable)

import pandas as pd
from config.config import RAW_FILE, SHEET_NAMES
from etl.logger import logger


def extract_data():
    logger.info("Iniciando extracción de datos.")

    data = pd.read_excel(RAW_FILE, sheet_name=SHEET_NAMES)

    for name, df in data.items():
        print(f"{name}: {len(df)} registros, {len(df.columns)} columnas")
        logger.info(f"{name}: {len(df)} registros cargados.")

    return data
