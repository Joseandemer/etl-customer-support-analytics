
# Modelo dimensional (Customer Support)

import pandas as pd
from etl.logger import logger


def _dimension_ids(
    df,
    natural_key,
    columns,
    surrogate_key,
    unknown
):
    dim = (
        df[[natural_key, *columns]]
        .dropna(subset=[natural_key])
        .drop_duplicates(subset=[natural_key])
        .sort_values(natural_key)
        .reset_index(drop=True)
    )

    dim.insert(
        0,
        surrogate_key,
        range(1, len(dim) + 1)
    )

    empty = {
        column: (
            pd.NaT if column.endswith("_date")
            else "No especificado"
        )
        for column in columns
    }

    empty.update({
        surrogate_key: 0,
        natural_key: unknown
    })

    return pd.concat(
        [pd.DataFrame([empty]), dim],
        ignore_index=True
    )


def _dimension_text(df, column, key_column, unknown):
    values = (
        df[column]
        .dropna()
        .astype("string")
        .unique()
        .tolist()
    )

    values = sorted(
        value for value in values
        if value != unknown
    )

    dim = pd.DataFrame({
        column: [unknown, *values]
    })

    dim.insert(
        0,
        key_column,
        range(0, len(dim))
    )

    return dim


def create_dimensions(data):
    logger.info("Creando dimensiones.")

    dim_agent = _dimension_ids(
        data["agents_raw"],
        "agent_id",
        [
            "agent_name",
            "team",
            "shift",
            "employment_status",
            "hire_date"
        ],
        "agent_key",
        "NO_ASIGNADO"
    )

    dim_customer = _dimension_ids(
        data["customers_raw"],
        "customer_id",
        [
            "customer_name",
            "segment",
            "city",
            "registration_date",
            "acquisition_channel"
        ],
        "customer_key",
        "NO_IDENTIFICADO"
    )

    tickets = data["tickets_raw"]

    dim_category = _dimension_text(
        tickets,
        "issue_category",
        "category_key",
        "Sin categoría"
    )

    dim_channel = _dimension_text(
        tickets,
        "channel",
        "channel_key",
        "No especificado"
    )

    # Dimensión calendario
    dates = (
        tickets["created_at"]
        .dropna()
        .dt.normalize()
    )

    calendar = pd.date_range(
        dates.min(),
        dates.max(),
        freq="D"
    )

    dim_date = pd.DataFrame({
        "date": calendar
    })

    dim_date["date_key"] = (
        dim_date["date"]
        .dt.strftime("%Y%m%d")
        .astype("int64")
    )

    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["day"] = dim_date["date"].dt.day

    dim_date = dim_date[
        [
            "date_key",
            "date",
            "year",
            "month",
            "month_name",
            "quarter",
            "day"
        ]
    ]

    return {
        "dim_agent": dim_agent,
        "dim_customer": dim_customer,
        "dim_category": dim_category,
        "dim_channel": dim_channel,
        "dim_date": dim_date
    }
