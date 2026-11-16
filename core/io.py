
# Framework ETL (Código reutilizable)

import os


def save_dataframe(df, folder, filename):
    os.makedirs(folder, exist_ok=True)

    output_path = os.path.join(folder, filename)

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d %H:%M:%S"
    )

    print(f"Archivo generado: {filename}")


def export_tables(tables, folder):
    for filename, dataframe in tables.items():
        save_dataframe(
            dataframe,
            folder,
            filename
        )

    print("\nTodas las tablas fueron exportadas correctamente.")
