import re
from bs4 import BeautifulSoup

class Extract_Competition_Text():

    #Initializes the variables and the class
    def __init__(self,company_name,file_path,year):
        self.company_name = company_name
        self.match_text = "COMPETITION"
        self.stop_text = "EMPLOYEES"
        self.file_path = file_path
        self.liability_flag = False
        self.stckhldrs_eq_flag = False
        self.debt_and_equity = {}
        self.year = year
 
    #Extracts "competition" text when the header "competition" is located in div tags
    def extract_text_for_div_tag(self,file_content):

        #Updating the stop text i.e. when to stop after parsing the entire competition text
        if self.company_name == "Tesla":
            updated_stop_text = "Intellectual Property"
        else:
            updated_stop_text = self.stop_text
        
        #used to set target_found flag. Used to find "competition" headline in the fillings
        target_found = False

        #parses all div contents
        parsed_file = BeautifulSoup(file_content, 'lxml')
        divs = parsed_file.find_all('div')
        redundant_text = ["item 1","part i","table of contents"]    #Redundant text initialized to not include while parsing
        passage = ""
        for div in divs:
            current_text = div.get_text(strip=True).lower()
            if current_text == self.match_text.lower(): #If competition header is found, set it true to start parsing the contents
                target_found = True
            elif current_text in redundant_text or current_text.isdigit():    #Skip redundant text
                continue
            elif target_found and current_text == updated_stop_text.lower():    #If stop text encountered, stop parsing
                break
            elif target_found:      #If competition header is found, keep on parsing until you encounter stop text
                passage += div.get_text(strip=True)
                passage += "\n"
        return passage
    
    #Extracts "competition" for the year 03 to 05 for MSFT
    def extract_text_from_03_to_05(self,file_content):

        passage = ""
        target_found = False
        stop_word_05 = "risk factors"
        redundant_text = ["item 1","part i","table of contents"]    #Redundant text initialized to not include while parsing
        with open(self.file_path, 'r') as file:
            file_content = file.read()

        #Parses all p tags
        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')

        for p in ps:
            current_text = p.get_text(strip=True).lower()   #If competition header is found, set it true to start parsing the contents
            if current_text == self.match_text.lower():     
                target_found = True
            elif current_text in redundant_text:    #Skip redundant text
                continue
            elif target_found and current_text == stop_word_05.lower():     #Stop word for year 2005 was unique
                break
            elif target_found and current_text==self.stop_text.lower():     #If stop text encountered, stop parsing
                break
            elif target_found:                  #If competition header is found, keep on parsing until you encounter stop text
                passage += p.get_text(strip=True)
                passage += "\n"
        return passage
    
    #extract "competition" passage from raw text i.e. without any html code
    def extract_competition_passage_from_raw_text(self):

        target_found = False
        passage = ""
        redundant_text = "<PAGE>"   #redundant text

        with open(self.file_path, 'r') as file:
            for line in file:
                if self.match_text.upper() == line.strip().upper():     #If competition header is found, set it true to start parsing the contents
                    target_found = True
                elif target_found and self.stop_text.upper() == line.strip().upper():   #If stop text encountered, stop parsing
                    break
                elif redundant_text in line.strip() or line.strip().isdigit():  #Skips redundant chars or words
                    continue
                elif target_found:      #If competition header is found, keep on parsing until you encounter stop text
                    passage += line
                    passage += "\n"
        return passage
    
    #Extracts the entire competition passage for Microsoft
    def extract_competition_passage_for_msft(self):

        with open(self.file_path, 'r') as file:
            file_content = file.read()
        
        #Extracts the passage from raw text
        if int(self.year) in range(1995,2002):
            passage = self.extract_competition_passage_from_raw_text()
            return passage
        
        #Extract passage from div tags
        if int(self.year) == 2002:
            passage = self.extract_text_for_div_tag(file_content)
            return passage
        
        #Extracts passages from unique stop words (not encountered in other years)
        if int(self.year) in range(2003,2006):
            passage = self.extract_text_from_03_to_05(file_content)
            return passage
        
        
        target_found = False
        passage = ""

        #Parsing p tags
        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')

        stop_text_current = "operations"    

        ignore_text = ["table of contents","part i","item 1"]   #Skips over

        """Competition text in these years, is a series of text followed by defn of products. We need to skip over the product's info
        #and only grab competition text"""
        for p in ps:
            current_text = p.get_text(strip=True).lower()   #extracts the current text from tags
            if current_text == self.match_text.lower():     #If competition header is found, set it true to start parsing the contents
                target_found = True
            elif p.find("u") or p.find("b"):        #Skips over products info section
                target_found = False
            elif target_found and current_text == stop_text_current.lower():    #stop parsing if you encounter stop word
                break
            elif current_text in ignore_text:       #skip over ignore words
                continue
            elif target_found:              #keep on parsing and adding the content into passage till you encounter stop word
                passage += p.get_text(strip=True)
                passage += "\n"

        return passage
    
    #Extract "competition passage" for TSLA
    def extract_competition_text_for_tsla(self):

        passage = ""
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        
        #In case the fillings consists of div tags for headers
        if self.year == "2024":
            return self.extract_text_for_div_tag(file_content)
        
        target_found = False

        parsed_file = BeautifulSoup(file_content, 'lxml')
        ps = parsed_file.find_all('p')
        stop_text = "Intellectual Property"

        for p in ps:
            current_text = p.get_text(strip=True).lower()   
            if current_text == self.match_text.lower():     #If competition header is found, set it true to start parsing the contents    
                target_found = True
            elif target_found and current_text == stop_text.lower():    #stop parsing if encounter stop word
                break
            elif target_found:
                passage += p.get_text(strip=True)       #keep on parsing and adding the content into passage till you encounter stop word
                passage += "\n"
        return passage
        

if __name__ == "__main__":
    etd = Extract_Competition_Text("TSLA","./sec-edgar-filings/TSLA/10-K/0001628280-24-002390/full-submission.txt","2024")  
    num = etd.extract_competition_text_for_tsla()
    print(num)

