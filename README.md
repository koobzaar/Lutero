<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_gov_horizontal_fundo_escuro.png">
      <source media="(prefers-color-scheme: light)" srcset="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_horizontal_fundo_transparente.png">
      <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_horizontal_fundo_transparente.png">
    </picture>
</p>

# Multifactorial Analysis of SARS-CoV-2 Mortality Data Consistency in Major World Health Organization Countries: A Newcomb-Benford Law and Demographic Indices Approach

## Introduction

The COVID-19 pandemic has generated a massive amount of epidemiological data, raising concerns about data integrity and accuracy. This research leverages Newcomb-Benford Law (NBL), a logarithmic distribution describing the expected frequency of leading digits in numerical datasets, to assess the consistency of COVID-19 mortality data across various countries. By examining the adherence of reported death tolls to NBL's expected pattern, the study aims to identify potential inconsistencies or anomalies that might indicate data quality issues.

## Key Research Points

### Newcomb-Benford Law (NBL)

* NBL posits that the probability of a digit 'd' (1 to 9) being the first digit in a number follows a logarithmic distribution: `P(d) = log10(1 + 1/d)`.
* This law has been widely used in various fields to detect fraud, validate data, and identify anomalies.

### COVID-19 Mortality Data Analysis

* The study focuses on daily COVID-19 mortality data from different countries, utilizing datasets from Johns Hopkins University, the Brazilian Ministry of Health, and the Centers for Disease Control and Prevention (CDC).
* Statistical tests, including tolerance limits with standard deviation and Mean Absolute Deviation (MAD), are employed to quantify the agreement between observed and expected digit frequencies.
* Factors influencing data adherence or deviation from NBL, such as sample size, data collection methodology, reporting policies, and demographic characteristics, are considered.

### Findings

* The analysis reveals varying degrees of adherence to NBL across different countries and data sources.
* Data from the Brazilian Consortium of Press Vehicles (CVI) showed significant deviations from NBL, raising concerns about its accuracy.
<p align="center">
    <img src="https://i.imgur.com/CjdlkgO.png">
</p>
* Data from Brazil's Ministry of Health exhibited moderate adherence, with some discrepancies observed.
* <p align="center">
    <img src="https://i.imgur.com/a6KJc5f.png" alt="Descrição da imagem">
</p>
* Japan demonstrated the highest level of conformity to NBL, suggesting data consistency.
<p align="center">
      <img src="https://i.imgur.com/iNJ0sCe.png" alt="Descrição da imagem">
</p>
* The United States data, despite limitations due to sample size, also showed relative adherence.
<p align="center">
    <img src="https://i.imgur.com/fByxG5j.png" alt="Descrição da imagem">
</p>
* Analysis of other countries, including France, Germany, Russia, and the United Kingdom, revealed varying patterns of adherence and deviations from NBL.
<p align="center">
    <img src="https://i.imgur.com/hgFvdJl.png" alt="Descrição da imagem">
</p>
* A global analysis of 128 countries highlighted regional disparities in NBL adherence, with Africa and Asia showing the greatest variability.
<p align="center">
      <img src="https://i.imgur.com/Be2OBqb.png" alt="Descrição da imagem">
      <img src="https://i.imgur.com/yV5y7Ne.png" alt="Descrição da imagem">
      <img src="https://i.imgur.com/dtNdVFc.jpeg" alt="Descrição da imagem">
</p>

* Japan and Montenegro exhibited the lowest deviation indices, suggesting high data consistency, while Vietnam and Congo Brazzaville showed the highest, indicating potential data quality issues.

## How to Use

The `main.py` script allows you to generate Benford Law plots and analyses for specific countries or all available countries in the dataset.

### Command-Line Arguments

* `--country [country_name]`:  Plots the Benford Law analysis for the specified country.
* `--all`: Plots Benford Law analyses for all available countries.
* `--cvi`: Calculates and plots only for the Brazilian Consortium of Press Vehicles (CVI) data.
* `--bms`: Calculates and plots only for the Brazilian Ministry of Health data.
* `--usa`: Calculates and plots only for the United States data.
* `--specific-countries [country1 country2 ...]`: Calculates and plots only for the listed specific countries.

### Example Usage

* Plot for Brazil (Ministry of Health data): `python main.py --bms`
* Plot for all countries: `python main.py --all`
* Plot for specific countries: `python main.py --specific-countries Japan France`

**Note:** Ensure that the required datasets are available in the specified paths within the script.

## Conclusion

This research underscores the potential of NBL as a tool for assessing data quality and identifying inconsistencies in COVID-19 mortality data. The findings highlight the importance of robust data collection and reporting practices during public health crises and contribute to the ongoing discussion on the applicability of NBL in real-world scenarios.

This article its not public yet.

## Authors

- @koobzaar (TRIGUEIRO, B. B.) - [Lattes](http://lattes.cnpq.br/2341132684122094) / [LinkedIn](https://www.linkedin.com/in/brunotrigueiro/). Atualmente vinculado a Faculdade de Tecnologia de São Paulo (Fatec-SP). Aluno em Análise e Desenvolvimento de Sistemas.
- **Orientador**: José Augusto Theodosio Pazetti (PAZETTI, J. A. T.) - [Lattes](http://lattes.cnpq.br/8445469805205594). Doutor em Ciências da Saúde pela Universidade Federal de São Paulo.
- **Coorientador**: Fernando Gonzales Tavares (in memoriam).

## Licence
Lutero © 2024 by Bruno Bezerra Trigueiro is licensed under Creative Commons Attribution-NonCommercial 4.0 International. To 
view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/
