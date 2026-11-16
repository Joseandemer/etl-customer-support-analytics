
import time

from etl.logger import logger
from etl.extract import extract_data
from etl.validate import validate_data
from etl.transform import transform_data
from etl.dimensions import create_dimensions
from etl.facts import create_fact_tickets
from etl.load import load_data


def main():
    start_time = time.time()

    try:
        print("=" * 50)
        print("INICIANDO ETL - CUSTOMER SUPPORT ANALYTICS")
        print("=" * 50)

        data = extract_data()

        validate_data(data)

        data = transform_data(data)

        dimensions = create_dimensions(data)

        fact_tickets = create_fact_tickets(
            data,
            dimensions
        )

        load_data(
            dimensions,
            fact_tickets
        )

        print("\nPIPELINE FINALIZADO CORRECTAMENTE")
        logger.info("Pipeline finalizado correctamente.")

    except Exception:
        logger.exception(
            "Error durante la ejecución del ETL."
        )
        raise

    finally:
        logger.info(
            f"Tiempo total: {time.time() - start_time:.2f} segundos"
        )


if __name__ == "__main__":
    main()
