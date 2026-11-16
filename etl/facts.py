
# Tabla de hechos (Customer Support)

import pandas as pd
from etl.logger import logger


def create_fact_tickets(data, dimensions):
    logger.info("Creando FactTickets.")

    fact = data["tickets_raw"].copy()

    # Relaciones con dimensiones
    relationships = [
        ("dim_agent", "agent_id", "agent_key"),
        ("dim_customer", "customer_id", "customer_key"),
        ("dim_category", "issue_category", "category_key"),
        ("dim_channel", "channel", "channel_key")
    ]

    for dimension, original_key, new_key in relationships:
        fact = fact.merge(
            dimensions[dimension][
                [original_key, new_key]
            ],
            on=original_key,
            how="left",
            validate="many_to_one"
        )

        fact[new_key] = (
            fact[new_key]
            .fillna(0)
            .astype("int64")
        )

    # Clave de fecha
    fact["date_key"] = pd.to_numeric(
        fact["created_at"].dt.strftime("%Y%m%d"),
        errors="coerce"
    ).astype("Int64")

    # Última encuesta válida por ticket
    surveys = (
        data["surveys_raw"]
        .dropna(subset=["csat_score", "survey_date"])
        .copy()
    )

    surveys = surveys.merge(
        fact[["ticket_id", "created_at"]],
        on="ticket_id",
        how="inner",
        validate="many_to_one"
    )

    surveys = surveys.loc[
        surveys["created_at"].notna()
        & (
            surveys["survey_date"]
            >= surveys["created_at"]
        )
    ]

    surveys = (
        surveys.sort_values(
            ["ticket_id", "survey_date", "survey_id"]
        )
        .drop_duplicates(
            subset=["ticket_id"],
            keep="last"
        )
    )

    fact = fact.merge(
        surveys[
            [
                "ticket_id",
                "survey_id",
                "survey_date",
                "csat_score"
            ]
        ],
        on="ticket_id",
        how="left",
        validate="one_to_one"
    )

    fact["ticket_count"] = 1

    fact = fact[
        [
            "ticket_id",
            "agent_key",
            "customer_key",
            "category_key",
            "channel_key",
            "date_key",
            "created_at",
            "first_response_at",
            "resolved_at",
            "status",
            "priority",
            "queue",
            "contact_type",
            "country",
            "reopen_count",
            "invalid_created_at",
            "ticket_count",
            "is_resolved",
            "first_response_hours",
            "resolution_hours",
            "first_response_sla_hours",
            "resolution_sla_hours",
            "sla_first_response_met",
            "sla_resolution_met",
            "survey_id",
            "survey_date",
            "csat_score"
        ]
    ]

    if fact["ticket_id"].duplicated().any():
        raise ValueError(
            "FactTickets contiene identificadores duplicados."
        )

    logger.info(
        f"FactTickets creada: {len(fact)} registros."
    )

    return fact
