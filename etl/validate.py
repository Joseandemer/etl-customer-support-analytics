
# Reglas de validación (Customer Support)

import pandas as pd
from etl.logger import logger
from rules.support_rules import (
    KEY_COLUMNS,
    DATE_COLUMNS,
    CSAT_MIN,
    CSAT_MAX
)


def validate_data(data):
    logger.info("Iniciando validación de datos.")

    for name, df in data.items():
        print(f"\nVALIDACIÓN: {name}")
        print(f"Filas: {len(df)} | Columnas: {len(df.columns)}")
        print(f"Duplicados exactos: {df.duplicated().sum()}")

        print("Nulos por columna:")
        nulls = df.isna().sum()
        nulls = nulls[nulls > 0]
        print(nulls.to_string() if not nulls.empty else "Sin nulos")

        key = KEY_COLUMNS[name]

        if key not in df.columns:
            raise ValueError(f"Falta la columna {key} en {name}")

        print(f"Identificadores duplicados ({key}): {df[key].duplicated().sum()}")

        for col in DATE_COLUMNS[name]:
            if col not in df.columns:
                raise ValueError(f"Falta la columna {col} en {name}")

            dates = pd.to_datetime(df[col], errors="coerce")
            invalid = dates.isna() & df[col].notna()

            print(f"Fechas no convertibles en {col}: {invalid.sum()}")

    tickets = data["tickets_raw"]
    customers = data["customers_raw"]
    agents = data["agents_raw"]
    surveys = data["surveys_raw"]

    print("\nREFERENCIAS")

    print(
        "Tickets con cliente inexistente:",
        (~tickets.customer_id.isin(customers.customer_id)).sum()
    )

    print(
        "Tickets sin agente:",
        tickets.agent_id.isna().sum()
    )

    print(
        "Encuestas con ticket inexistente:",
        (~surveys.ticket_id.isin(tickets.ticket_id)).sum()
    )

    scores = pd.to_numeric(
        surveys["csat_score"],
        errors="coerce"
    )

    invalid_csat = (
        scores.notna()
        & ~scores.between(CSAT_MIN, CSAT_MAX)
    )

    print(
        "Calificaciones fuera del rango CSAT:",
        invalid_csat.sum()
    )

    logger.info("Validación inicial finalizada.")

    return data
