import pandas as pd

df_driver = pd.read_excel("data_transportasi.xlsx", sheet_name="Driver", skiprows=1)
df_driver.columns = df_driver.columns.str.lower().str.strip()

print("Kolom yang berhasil dibaca:", df_driver.columns.tolist())
print("Isi data:")
print(df_driver.head())  # tampilkan 5 baris pertama


df_route = pd.read_excel("data_transportasi.xlsx", sheet_name="Route", skiprows=1)
df_route.columns = df_route.columns.str.lower().str.strip()

print("Kolom yang berhasil dibaca:", df_route.columns.tolist())
print("Isi data:")
print(df_route.head())  # tampilkan 5 baris pertama


df_trans = pd.read_excel("data_transportasi.xlsx", sheet_name="Transaction", skiprows=1)
df_trans.columns = df_trans.columns.str.lower().str.strip()

print("Kolom yang berhasil dibaca:", df_trans.columns.tolist())
print("Isi data:")
print(df_trans.head())  # tampilkan 5 baris pertama