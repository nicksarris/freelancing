__author__ = 'Nick Sarris (ngs5st)'

import pandas as pd
import numpy as np

stocks = pd.read_csv('AMEX_2007.csv')
print(stocks.sort(['symbol','date'], ascending=True))