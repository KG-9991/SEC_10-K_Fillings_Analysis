import re
from bs4 import BeautifulSoup

class Extract_Competition_Text():

    def __init__(self,company_name,file_path,year):
        self.company_name = company_name
        self.match_text = "COMPETITION"
        self.stop_text = "EMPLOYEES"
        self.file_path = file_path
        self.liability_flag = False
        self.stckhldrs_eq_flag = False
        self.debt_and_equity = {}
        self.year = year

    def extract_text_for_02(self,file_content):
        target_found = False

        parsed_file = BeautifulSoup(file_content, 'lxml')
        divs = parsed_file.find_all('div')
        passage = ""
        for div in divs:
            current_text = div.get_text(strip=True).lower()
            if current_text == self.match_text.lower():
                target_found = True
            elif target_found and current_text == self.stop_text.lower():
                break
            elif target_found:
                passage += div.get_text(strip=True)
                passage += "\n"
        return passage
    
    def extract_text_from_03_to_05(self,file_content):
        passage = ""
        target_found = False
        stop_word_05 = "risk factors"
        redundant_text = ["item 1","part i","table of contents"]
        with open(self.file_path, 'r') as file:
            file_content = file.read()

        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')

        for p in ps:
            current_text = p.get_text(strip=True).lower()
            if current_text == self.match_text.lower():
                target_found = True
            elif current_text in redundant_text:
                continue
            elif target_found and current_text == stop_word_05.lower():
                break
            elif target_found and current_text==self.stop_text.lower():
                break
            elif target_found:
                passage += p.get_text(strip=True)
                passage += "\n"
        return passage
    
    def extract_competition_passage_from_raw_text(self):
        target_found = False
        passage = ""
        redundant_text = "<PAGE>"
        with open(self.file_path, 'r') as file:
            for line in file:
                if self.match_text.upper() == line.strip().upper():
                    target_found = True
                elif target_found and self.stop_text.upper() == line.strip().upper():
                    break
                elif redundant_text in line.strip() or line.strip().isdigit():
                    continue
                elif target_found:
                    passage += line
                    passage += "\n"
        return passage
    
    def extract_competition_passage_for_msft(self):

        with open(self.file_path, 'r') as file:
            file_content = file.read()
        
        if int(self.year) in range(1995,2002):
            passage = self.extract_competition_passage_from_raw_text()
            return passage
        
        if int(self.year) == 2002:
            passage = self.extract_text_for_02(file_content)
            return passage
        
        if int(self.year) in range(2003,2006):
            passage = self.extract_text_from_03_to_05(file_content)
            return passage
        
        
        target_found = False
        passage = ""
        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')
        stop_text_current = "operations"
        ignore_text = ["table of contents","part i","item 1"]
        for p in ps:
            current_text = p.get_text(strip=True).lower()
            if current_text == self.match_text.lower():
                target_found = True
            elif p.find("u") or p.find("b"):
                target_found = False
            elif target_found and current_text == stop_text_current.lower():
                break
            elif current_text in ignore_text:
                continue
            elif target_found:
                passage += p.get_text(strip=True)
                passage += "\n"

        return passage
    
    def extract_competition_text_for_tsla(self):

        passage = ""
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        target_found = False

        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')
        stop_text = "Intellectual Property"
        for p in ps:
            current_text = p.get_text(strip=True).lower()
            if current_text == self.match_text.lower():
                target_found = True
            elif target_found and current_text == stop_text.lower():
                break
            elif target_found:
                passage += p.get_text(strip=True)
                passage += "\n"
        return passage
        

if __name__ == "__main__":
    etd = Extract_Competition_Text("TSLA","./sec-edgar-filings/TSLA/10-K/0001564590-17-003118/full-submission.txt","2017")  
    num = etd.extract_competition_text_for_tsla()
    print(num)  

