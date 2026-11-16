
# Transformaciones específicas (Customer Support)

import pandas as pd

from core.cleaner import (
    remove_duplicates,
    standardize_columns,
    trim_text_columns
)

from core.helpers import convert_to_datetime
from etl.logger import logger

from rules.support_rules import (
    DATE_COLUMNS,
    TEXT_COLUMNS,
    KEY_COLUMNS,
    PRIORITY_RULES,
    CHANNEL_RULES,
    CATEGORY_RULES,
    SLA_RULES,
    CSAT_MIN,
    CSAT_MAX
)


def normalize_labels(series, rules):
    lookup = {
        str(k).strip().casefold(): v
        for k, v in rules.items()
    }

    return series.astype("string").str.strip().map(
        lambda value: lookup.get(value.casefold(), value)
        if pd.notna(value) else pd.NA
    )


def transform_data(data):
    logger.info("Iniciando transformación de datos.")

    cleaned = {}

    # Limpieza general por fuente
    for name, original in data.items():
        df = original.copy()

        df = standardize_columns(df)
        df = trim_text_columns(df)
        df = remove_duplicates(df)
        df = convert_to_datetime(df, DATE_COLUMNS[name])

        for col in TEXT_COLUMNS[name]:
            df[col] = df[col].astype("string").str.strip()

        for col in [
            KEY_COLUMNS[name],
            "ticket_id",
            "customer_id",
            "agent_id"
        ]:
            if col in df.columns:
                df[col] = df[col].astype("string").str.strip()

        df = df.dropna(subset=[KEY_COLUMNS[name]])

        df = df.drop_duplicates(
            subset=[KEY_COLUMNS[name]],
            keep="last"
        )

        cleaned[name] = df.reset_index(drop=True)

    # Reglas específicas de tickets
    tickets = cleaned["tickets_raw"]

    tickets["status"] = tickets["status"].str.title()

    tickets["priority"] = normalize_labels(
        tickets["priority"],
        PRIORITY_RULES
    ).str.title()

    tickets["channel"] = normalize_labels(
        tickets["channel"],
        CHANNEL_RULES
    )

    tickets["issue_category"] = normalize_labels(
        tickets["issue_category"],
        CATEGORY_RULES
    )

    tickets["issue_category"] = (
        tickets["issue_category"].fillna("Sin categoría")
    )

    tickets["channel"] = (
        tickets["channel"].fillna("No especificado")
    )

    tickets["reopen_count"] = pd.to_numeric(
        tickets["reopen_count"],
        errors="coerce"
    )

    tickets["reopen_count"] = (
        tickets["reopen_count"]
        .mask(tickets["reopen_count"] < 0)
        .astype("Int64")
    )

    # Control de fechas inválidas
    now = pd.Timestamp.now()

    invalid_created = tickets["created_at"] > now

    tickets["invalid_created_at"] = (
        invalid_created.astype("Int64")
    )

    tickets.loc[
        invalid_created, "created_at"
    ] = pd.NaT

    for col in ["first_response_at", "resolved_at"]:
        invalid = (
            (tickets[col] > now)
            | (tickets[col] < tickets["created_at"])
        )

        tickets.loc[invalid, col] = pd.NaT

    # Cálculo de tiempos de atención
    tickets["first_response_hours"] = (
        (
            tickets["first_response_at"]
            - tickets["created_at"]
        ).dt.total_seconds() / 3600
    ).round(2)

    tickets["resolution_hours"] = (
        (
            tickets["resolved_at"]
            - tickets["created_at"]
        ).dt.total_seconds() / 3600
    ).round(2)

    tickets.loc[
        tickets["status"] != "Resuelto",
        "resolution_hours"
    ] = float("nan")

    # Objetivos de SLA según prioridad
    for target, field in [
        ("first_response_sla_hours", "first_response"),
        ("resolution_sla_hours", "resolution")
    ]:
        limits = {
            priority: values[field]
            for priority, values in SLA_RULES.items()
        }

        tickets[target] = tickets["priority"].map(limits)

    # Cumplimiento de SLA
    for result, hours, limit in [
        (
            "sla_first_response_met",
            "first_response_hours",
            "first_response_sla_hours"
        ),
        (
            "sla_resolution_met",
            "resolution_hours",
            "resolution_sla_hours"
        )
    ]:
        valid = (
            tickets[hours].notna()
            & tickets[limit].notna()
        )

        tickets[result] = pd.Series(
            pd.NA,
            index=tickets.index,
            dtype="Int64"
        )

        tickets.loc[valid, result] = (
            tickets.loc[valid, hours]
            <= tickets.loc[valid, limit]
        ).astype(int)

    tickets["is_resolved"] = (
        (tickets["status"] == "Resuelto")
        & tickets["resolved_at"].notna()
    ).astype("Int64")

    # Validación de encuestas
    surveys = cleaned["surveys_raw"]

    surveys["csat_score"] = pd.to_numeric(
        surveys["csat_score"],
        errors="coerce"
    )

    surveys.loc[
        ~surveys["csat_score"].between(
            CSAT_MIN,
            CSAT_MAX
        ),
        "csat_score"
    ] = float("nan")

    surveys["csat_score"] = (
        surveys["csat_score"].astype("Int64")
    )

    logger.info(f"Tickets preparados: {len(tickets)}")
    logger.info(f"Encuestas preparadas: {len(surveys)}")

    return cleaned
