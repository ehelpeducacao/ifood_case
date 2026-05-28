from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType, TimestampType

from src.config.settings import (
    REQUIRED_BASE_COLUMNS,
    YELLOW_DATETIME_COLUMNS,
    GREEN_DATETIME_COLUMNS
)


def validate_required_columns(df: DataFrame) -> None:
    """
    Valida se as colunas obrigatórias existem no DataFrame.

    Como o dataset contém Yellow Taxi e Green Taxi, as colunas de data/hora
    podem vir com prefixos diferentes:

    Yellow:
    - tpep_pickup_datetime
    - tpep_dropoff_datetime

    Green:
    - lpep_pickup_datetime
    - lpep_dropoff_datetime
    """

    missing_base_columns = [
        column for column in REQUIRED_BASE_COLUMNS
        if column not in df.columns
    ]

    if missing_base_columns:
        raise ValueError(
            f"As seguintes colunas obrigatórias estão ausentes no dataset: {missing_base_columns}"
        )

    has_yellow_datetime_columns = all(
        column in df.columns for column in YELLOW_DATETIME_COLUMNS
    )

    has_green_datetime_columns = all(
        column in df.columns for column in GREEN_DATETIME_COLUMNS
    )

    if not has_yellow_datetime_columns and not has_green_datetime_columns:
        raise ValueError(
            "O dataset não possui colunas válidas de data/hora. "
            "Esperado tpep_pickup_datetime/tpep_dropoff_datetime "
            "ou lpep_pickup_datetime/lpep_dropoff_datetime."
        )


def column_or_null(df: DataFrame, column_name: str):
    """
    Retorna a coluna se ela existir no DataFrame.
    Caso contrário, retorna nulo.
    """
    if column_name in df.columns:
        return F.col(column_name)

    return F.lit(None)


def standardize_taxi_data(df: DataFrame) -> DataFrame:
    """
    Padroniza os dados de Yellow Taxi e Green Taxi para um modelo único.

    Yellow Taxi usa:
    - tpep_pickup_datetime
    - tpep_dropoff_datetime

    Green Taxi usa:
    - lpep_pickup_datetime
    - lpep_dropoff_datetime

    A camada Silver usa nomes padronizados:
    - pickup_datetime
    - dropoff_datetime
    """

    return (
        df
        .withColumn(
            "pickup_datetime",
            F.coalesce(
                column_or_null(df, "tpep_pickup_datetime"),
                column_or_null(df, "lpep_pickup_datetime")
            ).cast(TimestampType())
        )
        .withColumn(
            "dropoff_datetime",
            F.coalesce(
                column_or_null(df, "tpep_dropoff_datetime"),
                column_or_null(df, "lpep_dropoff_datetime")
            ).cast(TimestampType())
        )
        .select(
            F.col("VendorID").cast(IntegerType()).alias("VendorID"),
            F.col("passenger_count").cast(DoubleType()).alias("passenger_count"),
            F.col("total_amount").cast(DoubleType()).alias("total_amount"),
            F.col("pickup_datetime"),
            F.col("dropoff_datetime")
        )
        .withColumn("pickup_date", F.to_date("pickup_datetime"))
        .withColumn("pickup_hour", F.hour("pickup_datetime"))
        .withColumn("pickup_month", F.date_format("pickup_datetime", "yyyy-MM"))
    )


def add_quality_validation_columns(df: DataFrame) -> DataFrame:
    """
    Aplica regras de qualidade e adiciona uma coluna com o motivo da rejeição.
    Quando rejection_reason for nulo, o registro é considerado válido.
    """

    return (
        df
        .withColumn(
            "rejection_reason",
            F.when(F.col("VendorID").isNull(), F.lit("VendorID is null"))
             .when(F.col("passenger_count").isNull(), F.lit("passenger_count is null"))
             .when(F.col("total_amount").isNull(), F.lit("total_amount is null"))
             .when(F.col("pickup_datetime").isNull(), F.lit("pickup datetime is null"))
             .when(F.col("dropoff_datetime").isNull(), F.lit("dropoff datetime is null"))
             .when(F.col("passenger_count") <= 0, F.lit("passenger_count must be greater than zero"))
             .when(F.col("passenger_count") > 6, F.lit("passenger_count greater than expected taxi capacity"))
             .when(F.col("total_amount") < 0, F.lit("total_amount must be greater than or equal to zero"))
             .when(F.col("total_amount") > 1000, F.lit("total_amount greater than expected threshold"))
             .when(
                 F.col("dropoff_datetime") < F.col("pickup_datetime"),
                 F.lit("dropoff datetime before pickup datetime")
             )
             .when(
                 ~F.col("pickup_month").between("2023-01", "2023-05"),
                 F.lit("pickup_month outside expected period")
             )
        )
    )


def get_valid_records(df: DataFrame) -> DataFrame:
    """
    Retorna apenas registros válidos.
    """
    return df.filter(F.col("rejection_reason").isNull()).drop("rejection_reason")


def get_invalid_records(df: DataFrame) -> DataFrame:
    """
    Retorna apenas registros inválidos com o motivo da rejeição.
    """
    return df.filter(F.col("rejection_reason").isNotNull())