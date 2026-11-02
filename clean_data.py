import pandas as pd

# 1. Load the original file
file_path = "N.-A-id-Ads-Oct-1-2026-Nov-1-2026.xlsx"
df = pd.read_excel(file_path)

# 2. Drop completely empty / redundant columns
df_clean = df.drop(
    columns=["Results (initial)", "Results (initial) indicator"], errors="ignore"
)

# 3. Fill missing numerical values with 0
df_clean["Results"] = df_clean["Results"].fillna(0)
df_clean["Cost per results"] = df_clean["Cost per results"].fillna(0)
df_clean["Result indicator"] = df_clean["Result indicator"].fillna("None")

# 4. Standardize Date columns
date_cols = ["Reporting starts", "Reporting ends"]
for col in date_cols:
    df_clean[col] = pd.to_datetime(df_clean[col]).dt.date

# 5. Clean ISO Timestamps
df_clean["Last significant edit"] = pd.to_datetime(
    df_clean["Last significant edit"], errors="coerce"
)

# 6. Calculate key metrics (CPM & CTR)
df_clean["CPM (PKR)"] = (
    df_clean["Amount spent (PKR)"] / df_clean["Impressions"]
) * 1000
df_clean["CTR (%)"] = (df_clean["Results"] / df_clean["Impressions"]) * 100

# 7. Export cleaned dataset
cleaned_file_path = "Cleaned_Ads_Data_Oct_2026.csv"
df_clean.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned successfully! Saved to {cleaned_file_path}")