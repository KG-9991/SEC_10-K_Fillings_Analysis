import streamlit as st
import os
import requests
from extract_debt_to_equity import Extract_Debt_To_Equity
from extract_competition_text import Extract_Competition_Text
import plotly.express as px
import numpy as np
import re
import time
#from sec_fillings_download import Download_Fillings


#Initializing session state for tracking analysis stages
if 'dte_analyzed' not in st.session_state:
    st.session_state['dte_analyzed'] = False

#Function to list subdirectories containing the 10-K filings
def list_subdirectories(directory):
    all_items = os.listdir(directory)
    subdirs = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]
    return subdirs

#Function to plot line graph depending on what type ofanalysis is being done
def plot_graph(years, ratios, type):
    if type=="DTE":     #For Debt To Equity
        x_legend = "Year"
        y_legend = "Debt-to-Equity Ratio"
        plot_title = 'Yearly Debt-to-Equity Ratios'
    elif type=="SEN":   #For Sentiment Analysis
        x_legend = "Year"
        y_legend = "Sentiment Score"
        plot_title = 'Sentiment Score Analysis'
    else:
        print("Invalid type - Please re-check")
        return None
    fig = px.line(
        x=years, y=ratios,
        labels={'x': x_legend, 'y': y_legend},
        title=plot_title
    )
    fig.update_traces(mode='lines+markers', marker=dict(size=8), line=dict(width=2))
    return fig

#Function to sort the dictionary by keys (years) and return sorted lists of years and their corresponding ratios
def sort_data(data):
    sorted_years = sorted(data.keys(), key=lambda x: int(x))  #Sorting the years numerically
    sorted_ratios = [data[year] for year in sorted_years]
    return sorted_years, sorted_ratios

#Function to fetch LLM Response from together.ai. Model used is Llama 3 8b-Chat
def get_llm_response(prompt):
    endpoint = 'https://api.together.xyz/v1/chat/completions'
    response = requests.post(endpoint, json={
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "max_tokens": 620,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [
            "<|eot_id|>"
        ],
        "messages": [
            {
                "content": prompt,
                "role": "user"
            }
        ]
    }, headers={
        "Authorization": "Bearer 50d122951c940a4202d30ba09d48967aa941cdce5cfb7d3d6dc66482effadebc",
    })
    
    if response.status_code == 200: #If the response is 200 i.e. success, fetching the content (text) of the response.
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Failed to fetch data: {response.status_code} {response.text}"

#Function to perform analysis for extracting yearwise dte ratios   
def perform_analysis_for_dte(company,directory):
    subdirectories = list_subdirectories(directory) #Listing the entire sub directories
    dte_vals = {}
    for sub_dir in subdirectories:
        year = sub_dir.split('-')[1]
        if int(year) in range(95,100):      #used for converting into year format i.e. yyyy
            year = "19" + year
        else:
            year = "20" + year
        file_path = f'{directory}/{sub_dir}/full-submission.txt'
        liab_and_equity = Extract_Debt_To_Equity(company, file_path,year)   #Creaing an object from Extract_Debt_To_Equity class to fetch dte ratios
        if company == "Tesla":
            dte_vals[year] = liab_and_equity.extract_dte_ratio_for_tesla()
        elif company == "Microsoft":
            dte_vals[year] = liab_and_equity.extract_debt_to_equity_ratio_for_msft()
        
    #Creating yearwise data for dte ratios
    yearwise_data_for_dte = {year: ratio for year, ratio in dte_vals.items()}

    return yearwise_data_for_dte

#creates passages as the extract function written in Extract_Competition_Text class
def create_passages_for_sentiment_score(company,directory):
    subdirectories = list_subdirectories(directory)
    passage_texts = {}
    for sub_dir in subdirectories:
        year = sub_dir.split('-')[1]

        #Converts into standard year format i.e. yyyy
        if int(year) in range(95,100):
            year = "19" + year
        else:
            year = "20" + year
        file_path = f'{directory}/{sub_dir}/full-submission.txt'
        competition_text = Extract_Competition_Text(company,file_path,year)
        if company == "Tesla":
            passage_texts[year] = competition_text.extract_competition_text_for_tsla()  #call to extract func for tsla
        elif company == "Microsoft":
            passage_texts[year] = competition_text.extract_competition_passage_for_msft()   #call to extract func for msft

    return passage_texts

#Function to create prompt for the llm for debt to equity analysis
def create_prompt_for_dte(company,dte_vals):
    #Sorting the dict 
    sorted_data_for_dte = {year: ratio for year, ratio in sorted(dte_vals.items())}
    formatted_values_for_dte = ', '.join([f"{year}: {ratio}" for year, ratio in sorted_data_for_dte.items()])   #Converting it to str to use it in prompt
    prompt_for_dte_ratio = f"Debt-to-equity ratios for {company} over consecutive years is: {formatted_values_for_dte}. Analyze the data and generate insights. Also mention why this ratio is improtant for an invester."
    return prompt_for_dte_ratio

#Creating llm responses for sentinment analysis task. Returns LLM responses and extracted sentiment scores yearwise in a form of dict.
def create_llm_responses_yearwise(company,passage_texts):

    #Generating LLM Responses
    llm_responses = {}
    sentiment_scores = {}
    for year,passage in passage_texts.items():
        prompt_for_sentiment_analysis = f"Compute Sentiment Score out of 1.0 for the text given below indicating how confident {company} is. Follow this output template without fail: Score: .\n <Your explanation for the rationale you used>. Text: {passage}"
        llm_response = get_llm_response(prompt_for_sentiment_analysis)
        score_search = re.search(r"Score:\s*(\d+\.\d+)", llm_response)      #Finding out matching text to extract sentiment from the response. 
        if score_search:
            score = float(score_search.group(1))
        else:
            print("Score not found in the response.")
        sentiment_scores[year] = score
        llm_responses[year] = llm_response
        time.sleep(2)       #To resolve Rate limiter issue for the API
    return llm_responses, sentiment_scores

def main():
    #Streamlit page setup

    #Downloading the sec-edgar fillings, not used currently since the app is already hosted on web server to avoid major delays.
    """company_tickers = ["MSFT","TSLA"]
    sec_10k = Download_Fillings(company_tickers)
    sec_10k.download_10k_filings()"""

    st.title('SEC 10-K Fillings Analysis')

    st.header("Debt to Equity Ratio Analysis")


    #Let user choose the company
    company = st.selectbox('Choose the company:', ['Tesla', 'Microsoft'])

    #Depending on company, setup the right directory
    if company == 'Tesla':
        directory = "./sec-edgar-filings/TSLA/10-K"
    elif company == 'Microsoft':
        directory = "./sec-edgar-filings/MSFT/10-K"

    #If the user clicks on analyze button, following processes will get executed i.e. Debt to Equity ratio analysis and Sentiment analysis
    if st.button('Analyze', key='analyze_button_for_dte_ratio'):
        with st.spinner('Please wait... Analyzing data. This might take few seconds as the data is quite huge.'):
            yearwise_dte_ratios = perform_analysis_for_dte(company,directory)

            #Used the sort function to get ordered lists for years and dte ratios
            years, ratios = sort_data(yearwise_dte_ratios)
            fig = plot_graph(years, ratios,"DTE")       #Plot line graph
            st.plotly_chart(fig, use_container_width=True)

            #Creates a prompt for fetching DTE Ratios
            prompt_for_dte_ratio = create_prompt_for_dte(company,yearwise_dte_ratios)

            #Fetches response for the prompt created above
            response = get_llm_response(prompt_for_dte_ratio)

            #Writes the response to the UI 
            st.write("LLM Insights:")
            st.write(response)
            st.session_state['dte_analyzed'] = True     #This makes session state - dte_analyzed set to true which enables the further execution of Sentiment Analysis.
            time.sleep(1)  # Pause the execution for 1 second - done for graceful execution for enhancing user expirience. (not a hard requiremnt though)
    
    if st.session_state['dte_analyzed']:    #Proceed only if previous section has executed.
        st.header("""Analysis of the tone for competitors in the fillings""")
        with st.spinner('Please wait... Analyzing data. This might take few seconds as the data is quite huge.'):

            #Extract competition passages from the fillings and aggregate them yearwise
            passage_texts = create_passages_for_sentiment_score(company,directory)

            #Generating LLM Responses
            llm_responses, sentiment_scores = create_llm_responses_yearwise(company,passage_texts)

            #Using the sort function to get ordered lists for years and sentinment scores
            years, score = sort_data(sentiment_scores)

            #Plots line for sentimnet scores over the consecutive years
            fig = plot_graph(years, score,"SEN")
            st.plotly_chart(fig, use_container_width=True)

            #Yearwise LLM response for the rationale:
            if company == "Tesla":
                year_span = range(2011,2025)
            elif company == "Microsoft":
                year_span = range(1995,2024)

            #Used for displaying yearwise sentinment scores
            for year in year_span:
                with st.expander(f"Rationale behind sentiment analyis for {year}"):
                    st.write("Score:",sentiment_scores[str(year)])
                    st.write("Rationale:",llm_responses[str(year)]) 
            st.session_state['dte_analyzed'] = False
            
if __name__ == "__main__":
    main()

