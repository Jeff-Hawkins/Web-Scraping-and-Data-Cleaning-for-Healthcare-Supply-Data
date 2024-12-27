import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

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
cleaned_file = '/path/to/Cleaned_Data.xlsx'
data.to_excel(cleaned_file, index=False)
print(f"Cleaned data saved to {cleaned_file}")

# Function to generate McKesson URL for a given item number
def generate_mckesson_url(item_no):
    return f"https://mms.mckesson.com/product/{item_no}?src=CS"

# Updated scraping function using requests and BeautifulSoup
def scrape_mckesson_data(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first table on the page
        table = soup.find('table')
        if not table:
            print(f"Table not found: {url}")
            return {'Mfr Name': None, 'Mfr item #': None}

        # Extract data from the table
        mfr_name = None
        mfr_item_no = None

        for row in table.find_all('tr'):
            header = row.find('th').text.strip()
            value = row.find('td').text.strip() if row.find('td') else None
            if header == "Manufacturer":
                mfr_name = value
            elif header == "Manufacturer #":
                mfr_item_no = value

        # Log the scraped result
        print(f"Scraped: {url} -> Mfr Name: {mfr_name}, Mfr item #: {mfr_item_no}")
        return {'Mfr Name': mfr_name, 'Mfr item #': mfr_item_no}
    except requests.exceptions.RequestException as req_err:
        print(f"HTTP error for {url}: {req_err}")
        return {'Mfr Name': None, 'Mfr item #': None, 'Error': str(req_err)}
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
        return {'Mfr Name': None, 'Mfr item #': None, 'Error': str(e)}

# Generate McKesson URLs for each row in your data
data['McKesson URL'] = data[item_column].apply(generate_mckesson_url)

# Filter rows where manufacturer data is missing
missing_data_rows = data[data['Mfr Name'].isna() | data[mfr_item_column].isna()]

# Log missing data rows
print(f"Rows with missing data: {len(missing_data_rows)}")
missing_data_rows.to_excel('/path/to/Missing_Data_Rows.xlsx', index=False)

# Prepare for parallel processing
batch_size = 50
batches = [missing_data_rows['McKesson URL'][i:i + batch_size] for i in range(0, len(missing_data_rows), batch_size)]

failed_urls = []  # Track URLs where scraping failed
results = []

# Use ThreadPoolExecutor to process batches in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_batch = {
        executor.submit(process_batch, batch.tolist(), idx + 1): idx
        for idx, batch in enumerate(batches)
    }
    for future in future_to_batch:
        batch_num = future_to_batch[future]
        try:
            batch_results = future.result()
            results.extend(batch_results)
        except Exception as e:
            print(f"Error processing batch {batch_num}: {e}")
            failed_urls.extend(batches[batch_num])

# Log failed URLs
if failed_urls:
    with open('/path/to/Failed_URLs.txt', 'w') as f:
        for url in failed_urls:
            f.write(url + '\n')
    print("Failed URLs logged to Failed_URLs.txt")

# Update original data with results
for result in results:
    url = result.get('url')
    mfr_name = result.get('Mfr Name')
    mfr_item_no = result.get('Mfr item #')

    # Match rows by URL and update data
    data.loc[data['McKesson URL'] == url, 'Mfr Name'] = mfr_name
    data.loc[data['McKesson URL'] == url, mfr_item_column] = mfr_item_no

# Save updated dataset
output_file = '/path/to/Updated_Mfg_Name_Search.xlsx'
data.to_excel(output_file, index=False)
print(f"Updated data saved to {output_file}")
