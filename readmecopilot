# Pandas ETL Pipeline

A Python-based ETL pipeline built with Pandas to clean, standardize, and transform a messy retail sales dataset into a structured, analysis-ready format.

This project focuses on automating data quality checks and normalization tasks such as detecting malformed values, filling missing entries, standardizing text formats, and converting inconsistent data into a consistent schema.

## Overview

The dataset used in this project contains messy, multi-source retail sales records with inconsistent formatting, missing values, and irregular entries. The pipeline applies automated cleansing rules to detect anomalies and standardize them before producing a clean dataset suitable for analysis.

The goal is to reduce manual data preparation time and improve data consistency with a repeatable ETL workflow.

## Key Operations

### 1. Flawed Data Detection
The pipeline identifies:
- Missing values
- Inconsistent formatting
- Invalid or malformed text entries
- Unstandardized numeric and categorical values

This is implemented using Pandas filtering techniques, conditional selection, and regular expressions (regex) to detect patterns that do not conform to the expected data structure.

### 2. Data Sanitization and Standardization
The project transforms flawed values into a uniform format using vectorized Pandas operations, including:
- `replace()`
- `fillna()`
- `apply()`
- regex-based cleaning
- value normalization for dates, numbers, and text fields

This helps convert messy entries into a consistent schema that is ready for downstream analysis or reporting.

## Tools and Technologies

- Language: Python 3.x
- Libraries:
  - Pandas
  - NumPy
  - `re` (Regular Expressions)
  - Word2Number
- Dataset: `retail_sales_messy.csv`
- Editor: Notepad++

## Project Structure

```text
Pandas-ETL-pipeline/
├── transform_data.py
├── retail_sales_messy.csv
├── README.md
└── output/
    └── cleaned_dataset.csv
