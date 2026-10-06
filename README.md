## Overview
​Custom Python ETL Pipeline using Pandas to ingest a messy, multi-source dataset, and apply automated cleansing and standardization protocols, reducing prep time by ~80%, and producing clean, uniform processed datasets usable to support decision-making and business analytics. 

## Key Operations
**Flawed Data Detection**:
Detecting missing or unformatted data using the Pandas "loc" function to apply filters constructed using regular expressions (regex).

**Sanitization and Standardized Formatting of Flawed Data Entries**:
Executed vectorized operations to sanitize missing data and applied unified structural schema across all data entries using Pandas methods such as replace, apply and fillna with regular expressions.

## Tools Used
* **Language:** Python 3.x
* **Libraries:** Pandas, Regex (`re`), Numpy, Word2Number
* **Dataset:** retail_sales_messy.csv
* **Environment:** Notepad++

## How to Run
1. Clone the Repository:
   ```bash
   git clone [https://github.com/osamaalioa2000-png/Pandas-ETL-pipeline.git]
    
2. Install Dependencies:
   ```bash
   pip install pandas numpy word2number

3. Run the ETL Script:
   ```bash
   python transform_data.py
   
