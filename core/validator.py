# Framework ETL (Código reutilizable)

import pandas as pd


def check_shape(df):
    """
    Muestra la cantidad de filas y columnas.
    """

    print("\n========== DATASET ==========")
    print(f"Filas     : {df.shape[0]}")
    print(f"Columnas  : {df.shape[1]}")


def check_dtypes(df):
    """
    Muestra los tipos de datos.
    """

    print("\n========== TIPOS DE DATOS ==========")
    print(df.dtypes)


def check_nulls(df):
    """
    Muestra la cantidad de valores nulos.
    """

    print("\n========== VALORES NULOS ==========")

    nulls = df.isnull().sum()

    print(nulls[nulls > 0])


def check_duplicates(df):
    """
    Cuenta registros duplicados.
    """

    duplicates = df.duplicated().sum()

    print("\n========== DUPLICADOS ==========")
    print(f"Registros duplicados: {duplicates}")


def check_negative_values(df, columns):
    """
    Valida columnas numéricas con valores negativos.

    Personalizar según el proyecto.
    """

    print("\n========== VALORES NEGATIVOS ==========")

    for column in columns:

        negatives = (df[column] < 0).sum()

        print(f"{column}: {negatives}")


def check_invalid_dates(df, columns):
    """
    Valida fechas no convertidas.

    Personalizar según el proyecto.
    """

    print("\n========== FECHAS INVÁLIDAS ==========")

    for column in columns:

        invalid = df[column].isna().sum()

        print(f"{column}: {invalid}")


def summary(df):
    """
    Resumen general del dataset.
    """

    print("\n========== RESUMEN ==========")

    print(df.describe(include="all"))