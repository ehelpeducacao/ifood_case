# iFood Case Técnico 

## 1. Objetivo

Este projeto implementa uma solução de Engenharia de Dados para ingestão, tratamento, validação, disponibilização e análise dos dados de corridas de táxi de Nova York, utilizando dados públicos da NYC Taxi & Limousine Commission.

O objetivo do desafio é:

- realizar a ingestão dos arquivos originais no Data Lake;
- processar os dados usando PySpark;
- disponibilizar os dados para consumo analítico;
- responder às perguntas propostas no estudo de caso;
- demonstrar boas práticas de Engenharia de Dados, qualidade de dados, modelagem em camadas e rastreabilidade.

---

## 2. Perguntas do desafio

As análises solicitadas são:

1. Qual a média de valor total (`total_amount`) recebido em um mês considerando todos os Yellow Taxis da frota?

2. Qual a média de passageiros (`passenger_count`) por cada hora do dia que pegaram táxi no mês de maio considerando todos os táxis da frota?

---

## 3. Fonte dos dados

Os dados utilizados são disponibilizados pela NYC Taxi & Limousine Commission:

```text
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page