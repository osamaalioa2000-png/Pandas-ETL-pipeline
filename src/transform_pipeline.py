import pandas as pd
import numpy as np
from word2number import w2n

def wtn(n):
	try:
		return str(w2n.word_to_num(n))
		
	except:
		return 'invalid'
		
	

def transform(input_path):
	df = pd.read_csv(input_path)
	df = df.drop_duplicates()
	df1 = df.copy()

	# TransactionID
	# standardizing format
	df['TransactionID'] = df['TransactionID'].str.replace(r'[^0-9]', '', regex=True)

	# Date
	# standardizing format
	wn = {'jan' : '01', 'feb' : '02', 'mar' : '03', 'apr' : '04', 'may' : '05', 'jun' : '06', 'jul' : '07', 'aug' : '08', 'sep' : '09', 'oct' : '10', 'nov' : '11', 'dec' : '12'}
	df['Date'] = df['Date'].str.lower().str.replace(r'/', '-', regex=True)
	df['Date'] = df['Date'].str.replace(r' ', '', regex=True)
	dates = df['Date'].str.split('-')
	dates0 = dates.str[0]
	dates1 = dates.str[1]
	dates2 = dates.str[2]
	# find dates that have the year at the end of the string and reverse them
	xxy_format = dates2.str.len() > 2
	temp = dates0.loc[xxy_format]
	dates0.loc[xxy_format] = dates2.loc[xxy_format]
	dates2.loc[xxy_format] = temp
	# find dates that have the month written as a word and replace the word with a number according to map wn
	dates1 = dates1.replace(wn)
	dates2 = dates2.replace(wn)
	# find dates that are in y-d-m format and reform them to y-m-d format
	ydm_format = dates1.astype(float) > 12
	temp = dates1.loc[ydm_format]
	dates1.loc[ydm_format] = dates2.loc[ydm_format]
	dates2.loc[ydm_format] = temp
	df['Date'] = pd.to_datetime(dates0 + '-' + dates1 + '-' + dates2, errors='coerce')

	# CustomerID
	# removing all non-numeric characters in customer id column (replacing with empty string '')
	df['CustomerID'] = df['CustomerID'].str.replace(r'[^0-9]', '', regex=True)

	# Product
	# removing all non-alphabetic characters and standardizing format in product column
	df['Product'] = df['Product'].str.lower().str.replace(r'[^a-z]', '', regex=True)
	df['Product'] = df['Product'].str.strip().str.lower().replace({'tabllet' : 'tablet', 'lapptop' : 'laptop'})
	df['Product'] = df['Product'].str.capitalize()

	# Category
	# standerdizing format
	df['Category'] = df['Category'].str.strip().str.lower().replace({'acc' : 'accessories'})
	df.loc[df['Category'].str[-1] != 's', 'Category'] += 's'
	df.loc[df['Category'] == 'electrnics', 'Category'] = 'electronics'
	df['Category'] = df['Category'].str.capitalize()
	df.loc[df['Product'] == 'Smartwatch', 'Category'] = 'Wearables'
	df.loc[df['Product'] == 'Headphones', 'Category'] = 'Accessories'
	df.loc[(df['Product'] == 'Laptop') | (df['Product'] == 'Smartphone') | (df['Product'] == 'Tablet'), 'Category'] = 'Electronics'

	# Quantity
	# removing alphabetic entries
	df.loc[df['Quantity'].fillna('1').str.isalpha(), 'Quantity'] = df['Quantity'].apply(wtn)
	df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(r'[^0-9-]', '', regex=True), errors='coerce')
	# print(df['Quantity'])

	# UnitPrice
	# standerdizing format
	df.loc[df['UnitPrice'].str.contains(r'USD|\$', na=False, regex=True), 'Currency'] = 'USD'
	df.loc[df['UnitPrice'].str.contains(r'€', na=False, regex=True), 'Currency'] = 'EU'
	df['UnitPrice'] = df['UnitPrice'].str.replace(r'[^0-9,.]', '', regex=True)
	df['UnitPrice'] = df['UnitPrice'].str.replace(r',', '.', regex=True)
	df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')

	# Discount
	# standardizing format
	not_perc = ~df['Discount'].str.contains(r'%', na=False, regex=True)
	df['Discount'] = df['Discount'].str.replace(r'[% ]', '', regex=True).astype(float)
	df.loc[not_perc, 'Discount'] *= 100
	df['Discount'] = df['Discount'].astype(str)
	not_nan = df['Discount'] != 'nan'
	df.loc[not_nan, 'Discount'] = df.loc[not_nan, 'Discount'] + '%'

	# PaymentMethod
	# standardizing format
	df['PaymentMethod'] = df['PaymentMethod'].str.lower().str.replace(r' ', '', regex=True)
	df.loc[df['PaymentMethod'].str.contains(r'credit|cc', na=False, regex=True), 'PaymentMethod'] = 'credit card'
	df.loc[df['PaymentMethod'].str.contains(r'debit', na=False, regex=True), 'PaymentMethod'] = 'debit card'
	df['PaymentMethod'] = df['PaymentMethod'].str.capitalize()

	# Region
	# standardizing format
	m = {'n' : 'North', 's' : 'South', 'e' : 'East', 'w' : 'West'}
	df['Region'] = df['Region'].str.lower().replace(r'[^a-z]', '', regex=True).map(m)

	# Email
	# standardizing format
	df['Email'] = df['Email'].str.replace('at', '@')
	df['Email'] = df['Email'].str.replace('dot', '.')
	df['Email'] = df['Email'].str.replace(' ', '')
	df['Email'] = df['Email'].str.replace(r'[][()]', '', regex=True)
	m1 = ['example', 'retailco', 'mail', 'shop']
	m2 = ['.com', '.io', '.org', '.net']
	no_domain = ~df['Email'].str.contains(r'\.(?:com|io|org|net)$', na=False, regex=True)
	for i in range(len(m1)):
		mask = no_domain & (df['Email'].str.contains(m1[i], na=False))
		df.loc[mask, 'Email'] = df.loc[no_domain, 'Email'] + m2[i]
		
	
	# extracting customerIDs from emails and filling missing CustomerID entries
	df.loc[df['CustomerID'].isna(), 'CustomerID'] = df['Email'].replace(r'[^0-9]', '', regex=True)

	# Returned
	# standardizing format
	df['Returned'] = df['Returned'].str.lower().map({'true' : 'Yes', 'false' : 'No', 'yes' : 'Yes', 'no' : 'No'})
	
	# filling missing Returned entries from Quantity column (Yes if Quantity < 0, No if Quantity >= 0)
	df.loc[(df['Quantity'] < 0) & (df['Returned'].isna()), 'Returned'] = 'Yes'
	df.loc[(df['Quantity'] >= 0) & (df['Returned'].isna()), 'Returned'] = 'No'

	# Notes
	# standardizing format
	df['Notes'] = df['Notes'].fillna('')
	df['Notes'] = df['Notes'].str.replace('—', '')
	df['Notes'] = df['Notes'].str.capitalize()
	df['Notes'] = df['Notes'].str.replace('asap', 'ASAP')

	df.to_csv(input_path + '_cleaned')
	

transform('retail_sales_messy.csv')
