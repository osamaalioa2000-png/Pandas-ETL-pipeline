import pandas as pd
import numpy as np
from word2number import w2n
from src.transform_pipeline import transform

file_name = 'retail_sales2.csv'
data = pd.read_csv('data/' + file_name)
cleaned_data = transform(data)
cleaned_data.to_csv('data/cleaned_' + file_name)
