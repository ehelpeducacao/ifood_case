# ============================================================
# Azure Storage Configuration
# ============================================================

STORAGE_ACCOUNT_NAME = "stdatalakeifoodcase"
CONTAINER_NAME = "datalakedev"

SECRET_SCOPE = "scope-access-sta"
SECRET_KEY = "azure-storage-sas-token"

AZURE_PROJECT_PREFIX = "ifood_case"
AZURE_LANDING_PREFIX = f"{AZURE_PROJECT_PREFIX}/landing/taxi"

# ============================================================
# Local Landing Path
# Usado apenas para baixar e ler os arquivos originais.
# As camadas Bronze, Silver, Quarantine e Quality e Gold serão tabelas gerenciadas.
# ============================================================

LOCAL_BASE_PATH = "/Workspace/Shared/ifood_case"

LOCAL_LANDING_PATH = f"{LOCAL_BASE_PATH}/landing/taxi"

LANDING_PATH = f"file:{LOCAL_LANDING_PATH}"

# ============================================================
# Database and Tables
# ============================================================

DATABASE_NAME = "ifood_case"

BRONZE_TABLE = f"{DATABASE_NAME}.bronze_taxi_trips"
SILVER_TABLE = f"{DATABASE_NAME}.silver_taxi_trips"
QUARANTINE_TABLE = f"{DATABASE_NAME}.quarantine_taxi_trips"

QUALITY_SUMMARY_TABLE = f"{DATABASE_NAME}.quality_summary_taxi_trips"
QUALITY_REJECTIONS_TABLE = f"{DATABASE_NAME}.quality_rejections_taxi_trips"

# ============================================================
# Data Contract
# ============================================================

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

# ============================================================
# Gold Managed Tables
# ============================================================

GOLD_DAILY_METRICS_TABLE = f"{DATABASE_NAME}.gold_daily_metrics"
GOLD_HOURLY_METRICS_TABLE = f"{DATABASE_NAME}.gold_hourly_metrics"


# ============================================================
# Source Files
# ============================================================

SOURCE_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

TAXI_TYPES = [
    "yellow",
    "green",
    "fhv", 
    "fhvhv"
]