
# Framework ETL (Código reutilizable)

from config.config import PROCESSED_FOLDER
from core.io import export_tables
from etl.logger import logger


def load_data(dimensions, fact_tickets):
    logger.info("Exportando tablas procesadas.")

    tables = {
        f"{name}.csv": df
        for name, df in dimensions.items()
    }

    tables["fact_tickets.csv"] = fact_tickets

    export_tables(tables, PROCESSED_FOLDER)

    logger.info("Exportación finalizada.")
