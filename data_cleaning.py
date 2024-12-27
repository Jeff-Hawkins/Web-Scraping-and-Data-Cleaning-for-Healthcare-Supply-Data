import pandas as pd

# Load the provided Excel file with the combined dataset
input_file = '/path/to/Combined_Data.xlsx'

# Load the combined data
data = pd.read_excel(input_file)

# Standardize column names by stripping leading/trailing spaces
data.columns = data.columns.str.strip()

# Dynamically determine the correct column name for item numbers
if 'Item #' in data.columns:
    item_column = 'Item #'
elif 'Item No.' in data.columns:
    item_column = 'Item No.'
else:
    raise KeyError("No valid item number column found in the data.")

# Dynamically detect the manufacturer item column name
if 'Mfr #' in data.columns:
    mfr_item_column = 'Mfr #'
elif 'Mfr item #' in data.columns:
    mfr_item_column = 'Mfr item #'
else:
    raise KeyError("No valid manufacturer item number column found in the data.")

# Convert item numbers to strings and handle invalid entries
data[item_column] = data[item_column].apply(
    lambda x: str(int(x)) if pd.notna(x) and str(x).replace(".0", "").isdigit() else None
)

# Drop rows with missing or invalid item numbers
data = data.dropna(subset=[item_column])

# Log the number of rows remaining after cleaning
print(f"Rows remaining after cleaning invalid item numbers: {len(data)}")

# Save cleaned data for verification
cleaned_file = '/path/to/Updated_Mfg_Name_Search.xlsx'
data.to_excel(cleaned_file, index=False)
print(f"Cleaned data saved to {cleaned_file}")
