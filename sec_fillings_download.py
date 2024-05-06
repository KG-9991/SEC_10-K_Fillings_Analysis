import os
from sec_edgar_downloader import Downloader

def download_10k_filings(company_tickers):
    # Initialize downloader instance
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    for company_ticker in company_tickers:
        if company_ticker == "MSFT":
            year_span = range(1995,2024)
        elif company_ticker == "TSLA":
            year_span = range(2011,2025)
        else:
            print(f"The date for the company {company_ticker} doesn't exist in sde-edgar-fillings")
            return
        # Loop through years from 1995 to 2023
        for year in year_span:
            # Construct the year string
            year_str = str(year)
            try:
                # Get 10-K filing for the given company ticker and year
                dl.get("10-K", company_ticker, after=f"{year_str}-01-01", before=f"{year_str}-12-31")
                print(f"Successfully downloaded 10-K filing for {company_ticker} in {year_str}")
            except Exception as e:
                print(f"Error downloading 10-K filing for {company_ticker} in {year_str}: {e}")

# List of company tickers (you can choose 2-3 companies or tickers of your choice)
company_tickers = ["MSFT","TSLA"]

# Download 10-K filings for each company ticker

download_10k_filings(company_tickers)
