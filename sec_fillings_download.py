import os
from sec_edgar_downloader import Downloader

#Download 10k fillings

class Download_Fillings():

    def __init__(self,company_tickers):
        self.company_tickers = company_tickers

    def download_10k_filings(self):

        #Initializes downloader instance
        dl = Downloader("MyCompanyName", "my.email@domain.com")
        for company_ticker in self.company_tickers:
            if company_ticker == "MSFT":
                year_span = range(1995,2024)
            elif company_ticker == "TSLA":
                year_span = range(2011,2025)
            else:
                print(f"The date for the company {company_ticker} doesn't exist in sde-edgar-fillings")
                return
            
            #Loop through years from 1995 to 2023
            for year in year_span:
                #Constructing the year string
                year_str = str(year)

                try:
                    #Fetch 10-K filing for the given company ticker and year
                    dl.get("10-K", company_ticker, after=f"{year_str}-01-01", before=f"{year_str}-12-31")
                    print(f"Successfully downloaded 10-K filing for {company_ticker} in {year_str}")
                except Exception as e:
                    print(f"Error downloading 10-K filing for {company_ticker} in {year_str}: {e}")


