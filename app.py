import streamlit as st
import os
import requests
from extract_debt_to_equity import Extract_Debt_To_Equity
from extract_competition_text import Extract_Competition_Text
import plotly.express as px
import numpy as np
import re

# Function to list subdirectories containing the 10-K filings
def list_subdirectories(directory):
    all_items = os.listdir(directory)
    subdirs = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]
    return subdirs

def plot_debt_to_equity(years, ratios):
    fig = px.line(
        x=years, y=ratios,
        labels={'x': 'Year', 'y': 'Debt-to-Equity Ratio'},
        title='Yearly Debt-to-Equity Ratios'
    )
    fig.update_traces(mode='lines+markers', marker=dict(size=8), line=dict(width=2))
    return fig

def sort_data(data):
    # Sort the dictionary by keys (years) and return sorted lists of years and their corresponding ratios
    sorted_years = sorted(data.keys(), key=lambda x: int(x))  # Ensuring the years are sorted numerically
    sorted_ratios = [data[year] for year in sorted_years]
    return sorted_years, sorted_ratios


def get_llm_response(prompt):
    

    endpoint = 'https://api.together.xyz/v1/chat/completions'
    response = requests.post(endpoint, json={
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "max_tokens": 512,
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
    
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Failed to fetch data: {response.status_code} {response.text}"
    
# Streamlit page setup
st.title('SEC 10-K Fillings Analysis')

st.header("Debt to Equity Analysis")
# Let user choose the company
company = st.selectbox('Choose the company:', ['Tesla', 'Microsoft'])

# Depending on company, setup the right directory
if company == 'Tesla':
    directory = "./sec-edgar-filings/TSLA/10-K"
elif company == 'Microsoft':
    directory = "./sec-edgar-filings/MSFT/10-K"

if st.button('Analyze', key='analyze_button_for_dte_ratio'):
    subdirectories = list_subdirectories(directory)
    dte_vals = {}
    #passage_texts = {}
    for sub_dir in subdirectories:
        year = sub_dir.split('-')[1]
        if int(year) in range(95,100):
            year = "19" + year
        else:
            year = "20" + year
        file_path = f'{directory}/{sub_dir}/full-submission.txt'
        liab_and_equity = Extract_Debt_To_Equity(company, file_path,year)
        #competition_text = Extract_Competition_Text(company,file_path,year)
        if company == "Tesla":
            dte_vals[year] = liab_and_equity.extract_dte_ratio_for_tesla()
            #passage_texts[year] = competition_text.extract_competition_text_for_tsla()
        elif company == "Microsoft":
            dte_vals[year] = liab_and_equity.extract_debt_to_equity_ratio_for_msft()
            #passage_texts[year] = competition_text.extract_competition_passage_for_msft()
    
    # Plotting the data
    yearwise_data_for_dte = {year: ratio for year, ratio in dte_vals.items()}

    # Use the sorting function to get ordered lists
    years, ratios = sort_data(yearwise_data_for_dte)
    fig = plot_debt_to_equity(years, ratios)
    st.plotly_chart(fig, use_container_width=True)


    #Creating the prompt
    sorted_data_for_dte = {year: ratio for year, ratio in sorted(dte_vals.items())}
    formatted_values_for_dte = ', '.join([f"{year}: {ratio}" for year, ratio in sorted_data_for_dte.items()])
    prompt_for_dte_ratio = f"Debt-to-equity ratios for {company} from 2011 to 2023 is: {formatted_values_for_dte}. Analyze the data and generate insights."
    # Call LLM with the extracted data
    response = get_llm_response(prompt_for_dte_ratio)
    st.write("LLM Insights:")
    st.write(response)

st.header("""Analysis of "Competition" text""")
if st.button('Analyze Text', key='analyze_button_for_sentiment'):
    subdirectories = list_subdirectories(directory)
    passage_texts = {}
    for sub_dir in subdirectories:
        year = sub_dir.split('-')[1]
        if int(year) in range(95,100):
            year = "19" + year
        else:
            year = "20" + year
        file_path = f'{directory}/{sub_dir}/full-submission.txt'
        competition_text = Extract_Competition_Text(company,file_path,year)
        if company == "Tesla":
            passage_texts[year] = competition_text.extract_competition_text_for_tsla()
        elif company == "Microsoft":
            passage_texts[year] = competition_text.extract_competition_passage_for_msft()

    #Generating LLM Responses
    llm_responses = {}
    sentiment_scores = {}

    for year,passage in passage_texts.items():
        prompt_for_sentiment_analysis = f"Compute Sentiment Score out of 1.0 for the text given below indicating how confident {company} is. Follow this output template without fail: Score: .\n <Your explanation for the rationale you used>. Text: {passage}"
        llm_response = get_llm_response(prompt_for_sentiment_analysis)
        score_search = re.search(r"Score:\s*(\d+\.\d+)", llm_response)
        if score_search:
            score = float(score_search.group(1))
        else:
            print("Score not found in the response.")
        sentiment_scores[year] = score
        llm_responses[year] = llm_response
    
    # Use the sorting function to get ordered lists
    years, score = sort_data(sentiment_scores)
    fig = plot_debt_to_equity(years, score)
    st.plotly_chart(fig, use_container_width=True)
    

    #Yearwise LLM response:
    if company == "Tesla":
        year_span = range(2011,2025)
    elif company == "Microsoft":
        year_span = range(1995,2023)
    
    selected_year = st.selectbox('Choose a specific year for LLM insights:', [str(year) for year in year_span])
    
    st.write(f"LLM Insights for the {selected_year}:")

    st.write(llm_responses[selected_year])


