import pandas as pd
import numpy as np
from src.transform_pipeline import transform

df = pd.from_csv('src.data.raw.csv')
transform(df)
