LOCAL_BASE_PATH = "/tmp/ifood_case"

LOCAL_LANDING_PATH = f"{LOCAL_BASE_PATH}/landing/taxi/"

LANDING_PATH = f"file:{LOCAL_BASE_PATH}/landing/taxi/"
BRONZE_PATH = f"file:{LOCAL_BASE_PATH}/bronze/taxi/"
SILVER_PATH = f"file:{LOCAL_BASE_PATH}/silver/taxi/"
QUARANTINE_PATH = f"file:{LOCAL_BASE_PATH}/quarantine/taxi/"
QUALITY_REPORT_PATH = f"file:{LOCAL_BASE_PATH}/quality/taxi/"

DATABASE_NAME = "ifood_case"

BRONZE_TABLE = f"{DATABASE_NAME}.bronze_taxi_trips"
SILVER_TABLE = f"{DATABASE_NAME}.silver_taxi_trips"
QUARANTINE_TABLE = f"{DATABASE_NAME}.quarantine_taxi_trips"

REQUIRED_BASE_COLUMNS = [
    "VendorID",
    "passenger_count",
    "total_amount"
]

YELLOW_DATETIME_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

GREEN_DATETIME_COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

SOURCE_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

SOURCE_FILES = [
    "yellow_tripdata_2023-01.parquet",
    "yellow_tripdata_2023-02.parquet",
    "yellow_tripdata_2023-03.parquet",
    "yellow_tripdata_2023-04.parquet",
    "yellow_tripdata_2023-05.parquet",
    "green_tripdata_2023-01.parquet",
    "green_tripdata_2023-02.parquet",
    "green_tripdata_2023-03.parquet",
    "green_tripdata_2023-04.parquet",
    "green_tripdata_2023-05.parquet"
]