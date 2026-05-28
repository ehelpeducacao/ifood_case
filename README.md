# iFood Case Técnico 

## 1. Objetivo do projeto

Este projeto implementa uma solução de Engenharia de Dados para ingestão, tratamento, validação, disponibilização e análise dos dados públicos de corridas de táxi de Nova York.

O case tem como objetivo demonstrar:

- ingestão de dados em uma arquitetura de Data Lake;
- uso de PySpark no processamento dos dados;
- organização dos dados em camadas;
- aplicação de regras de qualidade;
- separação de registros inválidos em quarentena;
- criação de uma camada Gold para consumo analítico;
- resposta às perguntas propostas no desafio técnico.

---

## 2. Perguntas respondidas

O projeto responde às seguintes perguntas do estudo de caso:

1. Qual a média de valor total (`total_amount`) recebido em um mês considerando todos os Yellow Taxis da frota?

2. Qual a média de passageiros (`passenger_count`) por cada hora do dia que pegaram táxi no mês de maio considerando todos os Yellow Taxis da frota?

---

## 3. Fonte dos dados

Os dados são disponibilizados pela NYC Taxi & Limousine Commission:

```text
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
```

Arquivos utilizados no projeto:

```text
yellow_tripdata_2023-01.parquet
yellow_tripdata_2023-02.parquet
yellow_tripdata_2023-03.parquet
yellow_tripdata_2023-04.parquet
yellow_tripdata_2023-05.parquet

green_tripdata_2023-01.parquet
green_tripdata_2023-02.parquet
green_tripdata_2023-03.parquet
green_tripdata_2023-04.parquet
green_tripdata_2023-05.parquet
```

Apesar das perguntas do desafio serem focadas em Yellow Taxi, o pipeline também ingere Green Taxi para demonstrar padronização de múltiplos schemas.

---

## 4. Arquitetura da solução

A solução foi organizada em camadas:

```text
Fonte NYC TLC
    |
    v
Landing
    |
    v
Bronze
    |
    v
Silver
    |
    +-------> Quarantine
    |
    v
Gold
    |
    v
Analytics SQL / PySpark
```

### Landing

Camada responsável por armazenar os arquivos originais baixados da fonte pública.

### Bronze

Camada inicial padronizada, criada a partir da Landing. Os arquivos Yellow Taxi e Green Taxi possuem diferenças de schema, por isso cada arquivo é lido individualmente e convertido para um schema comum antes da união.

### Silver

Camada de dados limpos, tratados e validados. Representa o menor granularidade analítica: uma linha por corrida válida.

### Quarantine

Camada que armazena os registros rejeitados pelas regras de qualidade, mantendo o motivo da rejeição.

### Gold

Camada de consumo analítico, criada a partir da Silver. Contém tabelas agregadas para facilitar consultas SQL e respostas analíticas.

---

## 5. Tecnologias utilizadas

```text
Python
PySpark
Spark SQL
Delta Lake
Databricks Community / Serverless
Azure Blob Storage
Azure Storage Blob SDK
Databricks Secret Scope
GitHub
```

---

## 6. Estrutura do projeto

```text
ifood-case/
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   └── quality/
│       └── quality_rules.py
│
├── notebooks/
│   ├── ingestion_to_land
│   ├── land_to_silver
│   ├── silver_to_gold
│   ├── 01_analysis_avg_total_amount_yellow_taxi
│   └── 02_analysis_avg_passenger_by_hour_may
│   └── 03_analysis_quality_quarentine
│
├── README.md
└── requirements.txt
```

---

## 7. Pré-requisitos

Antes de executar o projeto, é necessário ter:

- conta no Databricks Community Edition;
- repositório GitHub com os arquivos do projeto;
- Azure Storage Account criado;
- container criado no Azure Storage;
- SAS Token gerado para acesso ao container;
- Secret Scope criado no Databricks;
- Secret salvo no Databricks com o SAS Token.

Configuração esperada do secret:

```text
Scope: scope-access-sta
Secret: azure-storage-sas-token
```

---

## 8. Como clonar o repositório no Databricks

### Passo 1 — Acessar o Databricks

Acesse o Databricks Community Edition:

```text
https://community.cloud.databricks.com/
```

### Passo 2 — Abrir a área de Repos

No menu lateral do Databricks, acesse:

```text
Workspace > Repos
```

### Passo 3 — Clonar o repositório GitHub

Clique em:

```text
Add Repo
```

Informe a URL do repositório GitHub:

```text
https://github.com/ehelpeducacao/ifood_case.git
```

Depois clique em:

```text
Create Repo
```

### Passo 4 — Confirmar a estrutura

Após o clone, confira se a estrutura do projeto está parecida com:

```text
ifood-case/
├── src/
├── analysis/
├── README.md
└── requirements.txt
```

---

## 9. Configuração do projeto

As principais configurações ficam no arquivo:

```text
src/config/settings.py
```

Configuração utilizada:

```python
STORAGE_ACCOUNT_NAME = "stdatalakeifoodcase"
CONTAINER_NAME = "datalakedev"

SECRET_SCOPE = "scope-access-sta"
SECRET_KEY = "azure-storage-sas-token"
```

O SAS Token não é salvo no código. Ele é recuperado em tempo de execução usando:

```python
dbutils.secrets.get(
    scope="scope-access-sta",
    key="azure-storage-sas-token"
)
```

---

## 10. Instalação de dependências

No notebook `pipeline`, execute a primeira célula:

```python
%pip install azure-storage-blob
```

Essa biblioteca é usada para enviar os arquivos originais da Landing para o Azure Blob Storage.

---

## 11. Ordem de execução

Execute os notebooks nesta ordem:

```text
1. land_to_silver
2. silver_to_gold
3. 01_analysis_avg_total_amount_yellow_taxi
4. 02_analysis_avg_passenger_by_hour_may
4. 03_analysis_quality_quarentine
```

---

## 12. Execução do pipeline principal

O notebook principal é:

```text
land_to_silver
```

Ele executa as seguintes etapas:

```text
1. Criação do database
2. Remoção de tabelas antigas
3. Download dos arquivos da NYC TLC
4. Upload dos arquivos originais para Azure Blob Storage
5. Criação da camada Bronze
6. Criação da camada Silver
7. Criação da camada Quarantine
8. Criação dos relatórios de qualidade
```

Para executar, rode o notebook `land_to_silver` até o final.

A última célula executa:

```python
run_pipeline()
```

---

## 13. Execução da camada Gold

Após executar o pipeline principal, execute o notebook:

```text
silver_to_gold
```

Esse notebook cria a camada Gold a partir da Silver.

Ele gera as tabelas:

```text
ifood_case.gold_daily_metrics
ifood_case.gold_hourly_metrics
```

A última célula executa:

```python
run_gold_pipeline()
```

---

## 14. Execução das análises

Após gerar a Gold, execute os notebooks de análise.

### Análise 1

Notebook:

```text
analysis/01_analysis_avg_total_amount_yellow_taxi
```

Pergunta respondida:

```text
Qual a média de valor total total_amount recebido em um mês considerando todos os Yellow Taxis da frota?
```

### Análise 2

Notebook:

```text
analysis/02_analysis_avg_passenger_by_hour_may
```

Pergunta respondida:

```text
Qual a média de passageiros passenger_count por cada hora do dia que pegaram táxi no mês de maio considerando todos os Yellow Taxis da frota?
```

---

## 15. Explicação arquivo por arquivo

### 15.1 `src/config/settings.py`

Arquivo central de configuração do projeto.

Responsável por armazenar:

- nome do Storage Account;
- nome do container;
- nome do Secret Scope;
- nome da Secret Key;
- caminhos locais;
- nomes das tabelas gerenciadas;
- lista de arquivos de origem;
- contrato mínimo de colunas obrigatórias.

Principais configurações:

```python
STORAGE_ACCOUNT_NAME = "stdatalakeifoodcase"
CONTAINER_NAME = "datalakedev"

SECRET_SCOPE = "scope-access-sta"
SECRET_KEY = "azure-storage-sas-token"
```

Também define os arquivos que serão baixados:

```python
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
```

### 15.2 `src/quality/quality_rules.py`

Arquivo responsável pelas regras de qualidade e padronização da camada Silver.

Contém as funções:

#### `validate_required_columns`

Valida se o arquivo possui as colunas obrigatórias.

Como Yellow Taxi e Green Taxi usam nomes diferentes para as colunas de data, a função valida os dois cenários.

Yellow Taxi:

```text
tpep_pickup_datetime
tpep_dropoff_datetime
```

Green Taxi:

```text
lpep_pickup_datetime
lpep_dropoff_datetime
```

#### `standardize_taxi_data`

Padroniza os dados da Bronze para a Silver.

Cria colunas auxiliares:

```text
pickup_date
pickup_hour
pickup_month
```

#### `add_quality_validation_columns`

Aplica as regras de qualidade e adiciona a coluna:

```text
rejection_reason
```

Essa coluna indica por qual motivo o registro foi rejeitado.

#### `get_valid_records`

Retorna apenas registros válidos para a Silver.

#### `get_invalid_records`

Retorna os registros inválidos para a Quarantine.

### 15.3 `ingestion_to_land`

Notebook responsável pela ingestão inicial.

Ele executa três ações principais:

```text
1. Baixa os arquivos Parquet da NYC TLC
2. Salva os arquivos localmente
3. Envia os arquivos originais para o Azure Blob Storage
```

A função principal é:

```python
ingestion_to_landing()
```

Esse notebook não é executado isoladamente no fluxo principal. Ele é carregado dentro do notebook `land_to_silver`.

### 15.4 `land_to_silver`

Notebook principal do projeto.

Responsável por executar o pipeline de dados da Landing até a Quality.

Principais funções:

#### `create_database`

Cria o database:

```text
ifood_case
```

#### `drop_managed_tables_if_exists`

Remove tabelas antigas antes de uma nova execução.

Isso garante que o pipeline possa ser reprocessado sem conflito com tabelas anteriores.

#### `read_and_standardize_file`

Lê cada arquivo Parquet individualmente.

Essa abordagem foi adotada porque os arquivos Yellow Taxi e Green Taxi possuem diferenças de schema e tipos de dados entre meses.

Em vez de usar `mergeSchema`, o pipeline lê um arquivo por vez e padroniza os campos necessários.

#### `ingest_bronze`

Cria a tabela Bronze:

```text
ifood_case.bronze_taxi_trips
```

A Bronze contém os dados já padronizados tecnicamente, mas ainda sem aplicação das regras finais de qualidade.

#### `build_silver_and_quarantine`

Cria as tabelas:

```text
ifood_case.silver_taxi_trips
ifood_case.quarantine_taxi_trips
```

A Silver recebe os registros válidos.

A Quarantine recebe os registros rejeitados com o motivo da rejeição.

#### `generate_quality_report`

Cria as tabelas de qualidade:

```text
ifood_case.quality_summary_taxi_trips
ifood_case.quality_rejections_taxi_trips
```

Essas tabelas ajudam a auditar o resultado do pipeline.

#### `run_pipeline`

Orquestra a execução completa do pipeline principal.

### 15.5 `notebooks/silver_to_gold`

Notebook responsável por gerar a camada Gold.

A camada Gold é construída a partir da Silver.

Tabelas criadas:

```text
ifood_case.gold_daily_metrics
ifood_case.gold_hourly_metrics
```

#### `build_gold_daily_metrics`

Cria a tabela Gold diária.

Grão da tabela:

```text
pickup_date
pickup_month
taxi_type
```

Métricas geradas:

```text
total_trips
total_passengers
avg_passenger_count
sum_total_amount
avg_total_amount
first_pickup_datetime
last_pickup_datetime
created_at
```

#### `build_gold_hourly_metrics`

Cria a tabela Gold horária.

Grão da tabela:

```text
pickup_date
pickup_month
pickup_hour
taxi_type
```

Métricas geradas:

```text
total_trips
total_passengers
avg_passenger_count
sum_total_amount
avg_total_amount
first_pickup_datetime
last_pickup_datetime
created_at
```

#### `run_gold_pipeline`

Executa a geração completa da Gold.

### 15.6 `01_analysis_avg_total_amount_yellow_taxi`

Notebook analítico para responder à primeira pergunta do desafio.

Consulta a tabela:

```text
ifood_case.gold_daily_metrics
```

A média é calculada de forma ponderada:

```text
SUM(sum_total_amount) / SUM(total_trips)
```

Essa abordagem evita erro de média de médias.

### 15.7 `02_analysis_avg_passenger_by_hour_may`

Notebook analítico para responder à segunda pergunta do desafio.

Consulta a tabela:

```text
ifood_case.gold_hourly_metrics
```

A média de passageiros é calculada de forma ponderada:

```text
SUM(total_passengers) / SUM(total_trips)
```

---

## 16. Regras de qualidade

As regras aplicadas antes da criação da Silver são:

| Regra | Justificativa |
|---|---|
| `VendorID` não pode ser nulo | Identifica o fornecedor da corrida |
| `passenger_count` não pode ser nulo | Campo necessário para análise de passageiros |
| `total_amount` não pode ser nulo | Campo necessário para análise financeira |
| `pickup_datetime` não pode ser nulo | Campo necessário para análise temporal |
| `dropoff_datetime` não pode ser nulo | Campo necessário para consistência temporal |
| `passenger_count > 0` | Evita corridas sem passageiros |
| | `total_amount >= 0` | Evita distorção financeira |
| `total_amount <= 100000` | Evita outliers extremos |
| `dropoff_datetime >= pickup_datetime` | Garante consistência da corrida |
| `pickup_month` entre `2023-01` e `2023-05` | Garante aderência ao escopo do case |

---

## 17. Tabelas criadas

Após a execução completa, as seguintes tabelas são criadas:

```text
ifood_case.bronze_taxi_trips
ifood_case.silver_taxi_trips
ifood_case.quarantine_taxi_trips
ifood_case.quality_summary_taxi_trips
ifood_case.quality_rejections_taxi_trips
ifood_case.gold_daily_metrics
ifood_case.gold_hourly_metrics
```

---

## 18. Consultas finais

### 18.1 Média de valor total por mês para Yellow Taxi

```sql
SELECT
    pickup_month,
    ROUND(
        SUM(sum_total_amount) / SUM(total_trips),
        2
    ) AS avg_total_amount,
    SUM(total_trips) AS total_trips,
    ROUND(SUM(sum_total_amount), 2) AS sum_total_amount
FROM ifood_case.gold_daily_metrics
WHERE taxi_type = 'yellow'
  AND pickup_month BETWEEN '2023-01' AND '2023-05'
GROUP BY pickup_month
ORDER BY pickup_month;
```

### 18.2 Média de passageiros por hora em maio

```sql
SELECT
    pickup_hour,
    ROUND(
        SUM(total_passengers) / SUM(total_trips),
        2
    ) AS avg_passenger_count,
    SUM(total_trips) AS total_trips,
    ROUND(SUM(total_passengers), 2) AS total_passengers
FROM ifood_case.gold_hourly_metrics
WHERE pickup_month = '2023-05'
GROUP BY pickup_hour
ORDER BY pickup_hour;
```

---

## 19. Consultas úteis de qualidade

### Total de rejeições por mês, tipo e motivo

```sql
SELECT
    pickup_month,
    taxi_type,
    rejection_reason,
    SUM(rejected_records) AS total_rejections
FROM ifood_case.quality_rejections_taxi_trips
GROUP BY
    pickup_month,
    taxi_type,
    rejection_reason
ORDER BY
    pickup_month,
    taxi_type,
    total_rejections DESC;
```

### Total financeiro não computado por registros em quarentena

```sql
SELECT
    pickup_date,
    pickup_month,
    taxi_type,
    rejection_reason,
    COUNT(*) AS total_rejected_records,
    ROUND(SUM(passenger_count), 2) AS total_rejected_passengers,
    ROUND(SUM(total_amount), 2) AS total_amount_not_computed
FROM ifood_case.quarantine_taxi_trips
WHERE pickup_month BETWEEN '2023-01' AND '2023-05'
GROUP BY
    pickup_date,
    pickup_month,
    taxi_type,
    rejection_reason
ORDER BY
    pickup_date,
    taxi_type,
    total_amount_not_computed DESC;
```

### Detalhe dos registros em quarentena

```sql
SELECT
    VendorID,
    taxi_type,
    source_file,
    pickup_datetime,
    dropoff_datetime,
    pickup_date,
    pickup_hour,
    pickup_month,
    passenger_count,
    total_amount,
    rejection_reason,
    ingestion_timestamp
FROM ifood_case.quarantine_taxi_trips
WHERE pickup_month BETWEEN '2023-01' AND '2023-05'
ORDER BY
    pickup_date,
    taxi_type,
    rejection_reason,
    pickup_datetime;
```

---

## 20. Decisões técnicas

### Leitura individual dos arquivos

A leitura é feita arquivo por arquivo porque os datasets possuem diferenças de schema entre Yellow Taxi e Green Taxi.

Isso evita erros de `mergeSchema` e permite controlar explicitamente a conversão de tipos.

### Uso de Quarantine

Registros inválidos são armazenados em uma tabela de quarentena, e não descartados.

Isso permite:

- auditoria;
- rastreabilidade;
- análise de impacto;
- revisão de regras de qualidade;
- identificação de valores não computados.

### Uso da Gold

A Gold foi criada para consumo analítico.

Ela evita que consumidores finais precisem consultar a Silver diretamente ou conhecer todas as regras de cálculo.

### Cálculo correto das médias na Gold

Como a Gold é agregada, as médias devem ser calculadas de forma ponderada.

Correto:

```sql
SUM(sum_total_amount) / SUM(total_trips)
```

e:

```sql
SUM(total_passengers) / SUM(total_trips)
```

Evita-se usar:

```sql
AVG(avg_total_amount)
```

ou:

```sql
AVG(avg_passenger_count)
```

porque isso pode gerar média de médias.

---

## 21. Limitações conhecidas

O projeto foi desenvolvido considerando restrições do Databricks Community/Serverless.

Foram identificadas limitações para:

- escrita direta em `/FileStore`;
- leitura Spark em `file:/tmp`;
- escrita Delta em diretórios do `/Workspace`;
- uso de `spark.conf.set` para configurar credenciais Azure diretamente no Spark.

Por isso, a solução utiliza:

- Azure SDK para publicar a Landing no Azure Blob Storage;
- tabelas Delta gerenciadas no Databricks para Bronze, Silver, Quarantine, Quality e Gold.

Em um ambiente produtivo, recomenda-se:

- ADLS Gen2 com Hierarchical Namespace habilitado;
- Unity Catalog External Location;
- autenticação via Service Principal ou Managed Identity;
- escrita direta das camadas Delta no Data Lake;
- orquestração via Databricks Workflows.

---

## 22. Melhorias futuras

Possíveis evoluções da solução:

- criar testes automatizados com Pytest;
- adicionar validações de reconciliação Silver x Gold;
- criar dashboards sobre a camada Gold;
- publicar tabelas externas no ADLS Gen2;
- usar Databricks Workflows para orquestração;
- implementar monitoramento de qualidade;
- adicionar logs estruturados;
- versionar dados com Delta History;
- aplicar Auto Loader para ingestão incremental;
- adicionar particionamento e otimização física conforme volume.
