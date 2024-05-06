import re
from bs4 import BeautifulSoup

class Extract_Debt_To_Equity():

    def __init__(self,company_name,file_path,year):
        self.val = 1
        self.company_name = company_name
        self.liabilities = "Total liabilities"
        self.liabilities_and_equity = "Total liabilities and stockholders"
        self.stockholders_equity = "Total stockholders"
        self.file_path = file_path
        self.liability_flag = False
        self.stckhldrs_eq_flag = False
        self.debt_and_equity = {}
        self.year = year

    def extract_dte_ratio_for_tesla(self):
        
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        
        parsed_file = BeautifulSoup(file_content, 'lxml')
        tds = parsed_file.find_all('td')

        target_reached_liabilites_flag = False
        target_reached_equity_flag = False
        for td in tds:
            current_text = td.get_text(strip=True).lower()
            if target_reached_liabilites_flag and not self.liability_flag:
                # Check if the text in this td is just numbers
                if re.search(r'\d', current_text):
                    total_liability = int(current_text.replace(',', ''))
                    self.debt_and_equity["debt"] = total_liability
                    self.liability_flag = True
            else:
                # Look for the target text in this td
                if self.liabilities.lower() in td.get_text(strip=True).lower():
                    target_reached_liabilites_flag = True
                    
            if target_reached_equity_flag and not self.stckhldrs_eq_flag:
                # Check if the text in this td is just numbers
                if re.search(r'\d', current_text):
                    total_equity = int(current_text.replace(',', ''))
                    self.debt_and_equity["equity"] = total_equity
                    self.stckhldrs_eq_flag = True
            else:
                # Look for the target text in this td
                if self.stockholders_equity.lower() in current_text:
                    target_reached_equity_flag = True

        debt_to_equity_ratio = format(self.debt_and_equity["debt"]/self.debt_and_equity["equity"],".2f")
        return debt_to_equity_ratio
    
    def extract_dte_ratio_from_raw_text(self):
        target_reached_flag = False
        with open(self.file_path, 'r') as file:
            for line in file:
                if self.stockholders_equity in line and not target_reached_flag:
                    equity = line.split()[-1]
                    total_equity = int(equity.replace(",", ""))  # Remove commas if present
                    target_reached_flag = True
                if self.liabilities_and_equity in line:
                    liability_and_equity = line.split()[-1]
                    total_liability_and_equity = int(liability_and_equity[1:].replace(",", ""))
        total_debt = total_liability_and_equity - total_equity
        debt_to_equity_ratio = format(total_debt/total_equity,".2f")
        return debt_to_equity_ratio

    def extract_debt_to_equity_ratio_for_msft(self):
        if int(self.year) in range(1995,2002):
            dte_ratio = self.extract_dte_ratio_from_raw_text()
            return dte_ratio
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        
        parsed_file = BeautifulSoup(file_content, 'lxml')
        tds = parsed_file.find_all('td')

        target_reached_debt_and_eq_flag = False
        target_reached_equity_flag = False

        for td in tds:
            current_text = td.get_text(strip=True).lower()
            if target_reached_debt_and_eq_flag and not self.liability_flag:
                # Check if the text in this td is just numbers
                if re.search(r'\d', current_text):
                    total_liability_and_equity = int(current_text.replace(',', ''))
                    self.debt_and_equity["debt_and_equity"] = total_liability_and_equity
                    self.liability_flag = True
            else:
                # Look for the target text in this td
                if self.liabilities_and_equity.lower() in td.get_text(strip=True).lower():
                    target_reached_debt_and_eq_flag = True
                    
            if target_reached_equity_flag and not self.stckhldrs_eq_flag:
                # Check if the text in this td is just numbers
                if re.search(r'\d', current_text):
                    total_equity = int(current_text.replace(',', ''))
                    self.debt_and_equity["equity"] = total_equity
                    self.stckhldrs_eq_flag = True
            else:
                # Look for the target text in this td
                if self.stockholders_equity.lower() in current_text:
                    target_reached_equity_flag = True
        debt = self.debt_and_equity["debt_and_equity"] - self.debt_and_equity["equity"]
        debt_to_equity_ratio = format(debt/self.debt_and_equity["equity"],".2f")
        return debt_to_equity_ratio
        

             
if __name__ == "__main__":
    etd = Extract_Debt_To_Equity("MSFT","./sec-edgar-filings/MSFT/10-K/0001193125-14-289961/full-submission.txt","2014")  
    num = etd.extract_debt_to_equity_ratio_for_msft()
    print(num)  