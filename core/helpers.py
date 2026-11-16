# Framework ETL (Código reutilizable)

import os
import time
import pandas as pd


def create_directory(path):
    """
    Crea una carpeta si no existe.
    """

    os.makedirs(path, exist_ok=True)


def execution_time(start_time):

    """
    Calcula el tiempo de ejecución.
    """

    return round(time.time() - start_time, 2)


def dataframe_info(df):

    """
    Muestra información general del DataFrame.
    """

    print("\n========== DATASET ==========")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")
    print("=============================\n")


def convert_to_datetime(df, columns):

    """
    Convierte columnas a tipo fecha.

    Personalizar según el dataset del proyecto.
    """

    for column in columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df