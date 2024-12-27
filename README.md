# Web-Scraping-and-Data-Cleaning-for-Healthcare-Supply-Data
Web Scraping and Data Cleaning for Healthcare Supply Data

# Manufacturer Data Enrichment Project

## Overview

This project automates the process of cleaning and enriching manufacturer data from an Excel dataset. Missing details about manufacturers and their items are supplemented through web scraping from McKesson’s product pages. The enriched dataset can be used for inventory management, analytics, or other operational needs.

The workflow is divided into two sections: Data Cleaning and Web Scraping, providing a modular and efficient approach to processing large datasets.

## Features

### Data Cleaning
	•	Combines data from two Excel sheets (Summary - Bulk and Summary - PPD) into a unified dataset.
	•	Standardizes column names for consistency.
	•	Identifies and removes rows with invalid or missing item numbers.
	•	Outputs a cleaned version of the dataset for verification.

### Web Scraping
	•	Extracts missing manufacturer details (Mfr Name and Mfr item #) from McKesson’s product pages using requests and BeautifulSoup.
	•	Handles cases where web pages do not contain the required information and logs failed URLs.
	•	Processes data in batches for better efficiency and scalability.

### Logging and Outputs
	•	Logs rows with missing data for review.
	•	Generates a list of URLs that could not be scraped due to errors or missing information.
	•	Saves the final enriched dataset to an Excel file.

 ## Requirements

### 1. Python Environment
	•	Python 3.8 or higher

### 2. Required Libraries

Install the necessary Python libraries:

pip install requests beautifulsoup4 pandas openpyxl

### 3. Input Data
	•	The input Excel file should include:
	•	Two sheets: Summary - Bulk and Summary - PPD
	•	Required columns:
	•	Item # or Item No.: Unique item identifiers.
	•	Mfr Name: Manufacturer name.
	•	Mfr #: Manufacturer item number.

### 4. Network Access
	•	Ensure stable internet access to scrape data from McKesson product pages.

## How to Use

### 1. Prepare the Input File
	•	Save the input Excel file in the appropriate directory.
	•	Ensure the file contains two sheets (Summary - Bulk and Summary - PPD) with consistent column names.

### 2. Run the Script
	•	Execute the script in your Python environment:

 python script.py

### 3. Outputs

The script generates the following files in the specified directory:
####	1.	Combined_Data.xlsx: Cleaned and combined data from the input sheets.
####	2.	Missing_Data_Rows.xlsx: Rows with missing manufacturer details before scraping.
####	3.	Failed_URLs.txt: A text file listing URLs where scraping failed.
####	4.	Updated_Mfg_Name_Search.xlsx: Final enriched dataset with missing manufacturer details filled in.

## Code Breakdown

### 1. Data Cleaning

This section processes the input Excel file:
	•	Standardizes column names.
	•	Combines sheets into a single dataset while ensuring consistency in column names.
	•	Drops rows with missing or invalid item numbers.
	•	Saves an intermediate cleaned dataset for verification.

### 2. Web Scraping

This section handles fetching missing manufacturer details:
	•	Constructs McKesson product URLs based on item numbers.
	•	Scrapes data from product pages using requests and BeautifulSoup.
	•	Processes data in batches to optimize performance.
	•	Logs results for successful scrapes and URLs that failed.

## Project Structure

| File Name                     | Description                                                                                 |
|-------------------------------|---------------------------------------------------------------------------------------------|
| `script.py`                   | Main Python script to perform data cleaning and web scraping.                              |
| `Combined_Data.xlsx`          | Cleaned and combined dataset from input sheets. Ensures consistent column names and data.  |
| `Missing_Data_Rows.xlsx`      | Rows with missing data before the web scraping process. Useful for tracking and verification.|
| `Failed_URLs.txt`             | List of URLs where scraping failed. Can be used for troubleshooting or retrying scrapes.   |
| `Updated_Mfg_Name_Search.xlsx`| Final enriched dataset with manufacturer details filled in.                                |
| `README.md`                   | Project documentation, including an overview, usage instructions, and challenges.          |

## Example Results

### **Before Enrichment**
| Item #  | Description                   | Mfr Name       | Mfr #    |
|---------|-------------------------------|----------------|----------|
| 140705  | ADAPTER, PRESSURE LINE 22MM   | (blank)        | HUD1642  |
| 49176   | ALCOHOL, ISOPROPYL 70% 16OZ   | McKesson Brand | (blank)  |

### **After Enrichment**
| Item #  | Description                   | Mfr Name         | Mfr #    |
|---------|-------------------------------|------------------|----------|
| 140705  | ADAPTER, PRESSURE LINE 22MM   | Medline          | HUD1642  |
| 49176   | ALCOHOL, ISOPROPYL 70% 16OZ   | McKesson Brand   | 23-D0022 |

## Challenges and Solutions

### Challenges
####	1.	Data Inconsistencies:
	•	Input data had non-standard column names and missing item numbers.
	•	Solution: Standardized column names and removed invalid rows during cleaning.
####	2.	Failed Web Scrapes:
	•	Some URLs did not contain the required tables.
	•	Solution: Logged failed URLs for further review.
####	3.	Performance with Large Datasets:
	•	Large datasets slowed down the scraping process.
	•	Solution: Used parallel processing and batch execution.

## Future Improvements
	•	Implement retry logic for failed URL scrapes.
	•	Add a feature to scrape additional product information (e.g., descriptions, categories).
	•	Create a graphical user interface (GUI) for non-technical users.
	•	Optimize batch sizes dynamically based on system resources.
