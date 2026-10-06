import pandas as pd

data = pd.read_csv("messy_data.csv")
idata = data.copy()

data.columns = data.columns.str.replace(r"[/(/)/$]", "", regex=True)

mask = data["Name"].isna()
data.loc[mask, "Name"] = data["Email"].str.split("@").str[0]
data["Name"] = data["Name"].str.replace(r"[/@]", "a", regex=True)
data["Name"] = data["Name"].str.strip()
data["Name"] = data["Name"].str.lower()
data["Name"] = data["Name"].str[0].str.upper() + data["Name"].str[1:]

data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
data["Age"].fillna(data["Age"].mean(), inplace=True)
data["Age"] = data["Age"].astype(int)

data["Salary"].fillna(data["Salary"].mean(), inplace=True)

data["Department"].fillna(data["Department"].mode()[0], inplace=True)

data["Joining Date"] = data["Joining Date"].str.replace(r"[/]", "-", regex=True)
data["Joining Date"] = data["Joining Date"].str.replace(r"[ ]", "", regex=True)
mask = data["Joining Date"].str.split("-").str[-1].astype(float) > 31
data.loc[mask, "Joining Date"] = data["Joining Date"].str.split("-").str[::-1].str.join("-")
mask = data["Joining Date"].str.split("-").str[1].astype(float) > 12
# data.loc[mask, "Joining Date"] = data["Joining Date"].str.split("-").str[0] + '-' + data["Joining Date"].str.split("-").str[2] + '-' + data["Joining Date"].str.split("-").str[1]
print(data["Joining Date"].str.split("-"))
data.loc[mask, "Joining Date"] = data["Joining Date"].str.split("-").apply(lambda x: x[0] + "-" + x[2] + "-" + x[1] if type(x) == list else 0)
data["Joining Date"] = pd.to_datetime(data["Joining Date"], errors="coerce")

data["Email"].fillna("noemail", inplace=True)
mask = (data["Email"].str[-4:] != ".com") & (data["Email"] != "noemail")
data.loc[mask, "Email"] = data["Email"] + ".com"
data["Email"] = data["Email"].str.replace("at", "@")
data["Email"] = data["Email"].str.replace(r"[][()]", "", regex=True)

df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz'],
                    'value': [1, 2, 3]})
df2 = pd.DataFrame({'rkey': ['baz', 'bar', 'foo'],
                    'value': [5, 6, 7]})


print(idata, "\n")
print(data)

print(df1)
print(df2)
print(df1.set_index("lkey").merge(df2.set_index("rkey"), left_on="lkey", right_on="rkey"))