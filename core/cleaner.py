# Framework ETL (Código reutilizable)

import pandas as pd


def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    print(f"Duplicados eliminados: {removed}")

    return df


def standardize_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


def trim_text_columns(df):

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:

        df[column] = df[column].str.strip()

    return df


def standardize_text(df, columns):
    """
    Convierte texto al formato Título.

    Personalizar las columnas según el proyecto.
    """

    for column in columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.title()
        )

    return df


def replace_values(df, column, replacements):
    """
    Reemplaza valores utilizando un diccionario.

    Personalizar según las reglas del proyecto.
    """

    df[column] = df[column].replace(replacements)

    return df


def remove_negative_values(df, columns):
    """
    Convierte valores negativos en nulos.

    Personalizar según el proyecto.
    """

    for column in columns:

        df.loc[df[column] < 0, column] = pd.NA

    return df