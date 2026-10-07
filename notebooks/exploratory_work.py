import pandas as pd
import numpy as np
from word2number import w2n


def wtn(n):
	try:
		return str(w2n.word_to_num(n))
		
	except:
		return "invalid"
		
	

df = pd.read_csv("retail_sales_messy.csv")
df = df.drop_duplicates()
df1 = df.copy()

# TransactionID
df["TransactionID"] = df["TransactionID"].str.replace(r"[^0-9]", "", regex=True)
# print(df["TransactionID"].unique())

# date
wn = {"jan" : 1, "feb" : 2, "mar" : 3, "apr" : 4, "may" : 5, "jun" : 6, "jul" : 7, "aug" : 8, "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}
df["Date"] = df["Date"].str.replace(r"[/]", "-", regex=True)
df["Date"] = df["Date"].str.replace(r"[ ]", "", regex=True)
mask = df["Date"].str.split("-").str[-1].astype(float) > 31
df.loc[mask, "Date"] = df["Date"].str.split("-").str[::-1].str.join("-")
mask = df["Date"].str.split("-").str[1].str.lower().isin(wn.keys())
df.loc[mask, "Date"] = df.loc[mask, "Date"].str.split("-").apply(lambda x: "{}-{}-{}".format(x[0], wn[x[1].lower()], x[2]))
mask = df["Date"].str.split("-").str[1].astype(float) > 12
df.loc[mask, "Date"] = df["Date"].str.split("-").str[0] + '-' + df["Date"].str.split("-").str[2] + '-' + df["Date"].str.split("-").str[1]
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
# print(df["Date"].unique())

# CustomerID
df["CustomerID"] = df["CustomerID"].str.replace(r"[^0-9]", "", regex=True)

# Product
df["Product"] = df["Product"].str.lower().str.replace(r"[^a-z]", "", regex=True)
df["Product"] = df["Product"].str.strip().str.lower().replace({"tabllet" : "tablet", "lapptop" : "laptop"})
df.loc[~df["Product"].isna(), "Product"] = df.loc[~df["Product"].isna(), "Product"].apply(lambda x: x[0].upper() + x[1:])
# print(df["Product"].unique())

# Category
df["Category"] = df["Category"].str.strip().str.lower().replace({"acc" : "accessories"})
df.loc[df["Category"].str[-1] != "s", "Category"] += "s"
df.loc[df["Category"] == "electrnics", "Category"] = "electronics"
df.loc[~df["Category"].isna(), "Category"] = df.loc[~df["Category"].isna(), "Category"].apply(lambda x: x[0].upper() + x[1:])
df.loc[df["Product"] == "Smartwatch", "Category"] = "Wearables"
df.loc[df["Product"] == "Headphones", "Category"] = "Accessories"
df.loc[(df["Product"] == "Laptop") | (df["Product"] == "Smartphone") | (df["Product"] == "Tablet"), "Category"] = "Electronics"
# print(df["Category"].unique())

# Quantity
df.loc[df["Quantity"].fillna("1").str.isalpha(), "Quantity"] = df["Quantity"].apply(wtn)
df["Quantity"] = pd.to_numeric(df["Quantity"].str.replace(r"[^0-9-]", "", regex=True), errors="coerce")
# print(df["Quantity"].unique())

# UnitPrice
df.loc[df["UnitPrice"].str.contains(r"[(USD)($)]", na=False, regex=True), "Currency"] = "USD"
df.loc[df["UnitPrice"].str.contains(r"€", na=False), "Currency"] = "EU"
df["UnitPrice"] = df["UnitPrice"].str.replace(r"[^0-9,.]", "", regex=True)
# df["UnitPrice"] = df["UnitPrice"].str.replace(r",", ".", regex=True).str.split(".").apply(lambda x: "".join(x[:-1]) + "." + x[-1] + "0" * (2 - len(x[-1])) if type(x) != float else x).astype(float)
df["UnitPrice"] = df["UnitPrice"].str.replace(r",", ".", regex=True)
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
# print(df["UnitPrice"].unique())

# Discount
df["Discount"] = df["Discount"].str.replace(r"[% ]", "", regex=True).astype(float)
df.loc[df["Discount"] <= 1, "Discount"] *= 100
df["Discount"] = df["Discount"].fillna("nan")
df.loc[df["Discount"] != "nan", "Discount"] = df["Discount"].astype(str) + "%"
df["Discount"] = df["Discount"].replace("nan", np.nan)
# df.loc[~df["Discount"].isna(), "Discount"] = df.loc[~df["Discount"].isna(), "Discount"].astype(str) + "%"
# print(df["Discount"].unique())

# Total
# print(df["Total"].unique())
# print((df["Quantity"]) * (df["UnitPrice"]) * (1 - (df["Discount"].str[:-1].astype(float) / 100)))
# print(df[["Quantity", "UnitPrice", "Discount", "Total"]])

# PaymentMethod
df["PaymentMethod"] = df["PaymentMethod"].str.lower().str.replace(r" ", "", regex=True)
df.loc[df["PaymentMethod"].str.contains(r"(credit)|(cc)", na=False, regex=True), "PaymentMethod"] = "credit card"
df.loc[df["PaymentMethod"].str.contains(r"(debit)", na=False, regex=True), "PaymentMethod"] = "debit card"
df["PaymentMethod"] = df["PaymentMethod"].apply(lambda x: x[0].upper() + x[1:] if type(x) == str else x)
# print(df["PaymentMethod"].unique())

# Region
m = {"n" : "North", "s" : "South", "e" : "East", "w" : "West"}
# df["Region"] = df["Region"].str.lower().str.replace(r"[^a-z]", "", regex=True).loc[~df["Region"].isna()].apply(lambda x: m[x] if len(x) == 1 else x[0].upper() + x[1:])
df["Region"] = df["Region"].str.lower().replace(r"[^a-z]", "", regex=True).map(m).fillna(df["Region"].str.capitalize())
# print(df["region"].unique())

# Email
df["Email"] = df["Email"].str.replace("at", "@")
df["Email"] = df["Email"].str.replace("dot", ".")
df["Email"] = df["Email"].str.replace(" ", "")
df["Email"] = df["Email"].str.replace(r"[][()]", "", regex=True)
m = {"example" : ".com", "retailco" : ".io", "mail" : ".org", "shop" : ".net"}
df.loc[~df["Email"].str.contains(r"(.com)|(.io)|(.org)|(.net)", na=False, regex=True), "Email"] = df.loc[~df["Email"].str.contains(r"(.com)|(.io)|(.org)|(.net)", na=False, regex=True), "Email"].apply(lambda x: x + m[x[x.index("@") + 1:]] if type(x) == str else x)
# print(df["Email"].apply(lambda x: x[x.index("@") + 1:] if type(x) == str else x).unique())
# print(df["Email"].unique())

# filling CustomerID from Email
df.loc[df["CustomerID"].isna(), "CustomerID"] = df["Email"].replace(r"[^0-9]", "", regex=True)
# print((df["CustomerID"] == df["Email"].replace(r"[^0-9]", "", regex=True)).value_counts())

# Returned
df["Returned"] = df["Returned"].str.lower().map({"true" : "Yes", "false" : "No", "yes" : "Yes", "no" : "No"})
# print(df["Returned"].unique())

# Notes
df['Notes'] = df['Notes'].fillna('')
df['Notes'] = df['Notes'].str.replace('—', '')
df['Notes'] = df['Notes'].str.replace('asap', 'ASAP')
df['Notes'] = df['Notes'].apply(lambda x: ' '.join([i[0].upper() + i[1:] for i in x.split() if len(x) > 0]))
# print(df['Notes'].unique())

df.to_csv("cleaned_data.csv")
# print(df.columns)
# print(df1, "\n")
# print(df)
