# Apartment Listing Scraper

## Overview
This script is designed to scrape apartment listing data from a Spanish real estate web portal. It uses Selenium to navigate the website, extract relevant information, and store it in a CSV file for further analysis.

## Features
- Automated login to Google for any additional access requirements.
- Scraping functionality that navigates through the listings, collecting apartment features and links.
- Utilization of various request headers to mimic genuine browser requests.
- Smooth scrolling through pages to ensure all dynamically loaded content is captured.
- Saves the scraped data into a Pandas DataFrame and outputs to a CSV file.

## Prerequisites
- Python 3
- Selenium
- Pandas

## Installation
1. Clone this repository or download the script.
2. Install the required Python libraries:
    ```bash
    pip install selenium pandas
    ```
3. Download the appropriate WebDriver for your browser and ensure it's available in your PATH.

## Usage
1. Update the `login_to_google` function with your Google credentials.
2. Set the desired parameters for `page_number`, `sell_or_rent`, and `capital` in the `main` function as per your scraping needs.
3. Modify the CombinedLocationIDs, latitude and longitude parameters accordingly to your search area, see image below:

![Apartment Listings](https://raw.githubusercontent.com/SergiDataAnalyst/scrapping_appartment_website/main/Network%20Tab.png)


## Data Output
The script outputs the data into a CSV file named `articles_data.csv`, containing columns for links, features, and icon features of the apartment listings.

## Disclaimer
Web scraping can be against the Terms of Service of some websites. Use this script responsibly and ethically, and ensure you have permission to scrape the desired website. This code is only for educating purposes.
