# SEC_10-K_Fillings_Analysis
Text Analysis of SEC 10-K Fillings using Llama 3 8b-Chat (from together.ai) for Tesla and Microsoft

## Analysis was conducted on two main insights - Debt to Equity Ratio and Analysis of tone of the company for the competitors

## 1. Debt to Equity Ratio:
    What is Debt to Equity Ratio?

    The debt-to-equity ratio (D/E) is a financial metric used to assess a company's financial leverage by comparing its total    
    liabilities to its shareholder equity. This ratio is calculated by dividing a company’s total liabilities by its shareholder 
    equity. 
    
    The debt-to-equity ratio is useful for investors for several reasons:

    1. It helps investors understand how much a company is financing its operations through debt versus wholly owned funds. A   
       high ratio implies more debt, which could be risky if the company faces financial difficulties.
    
    2. It provides insights into the company’s financial health and stability. Companies with a sustainable amount of debt 
       relative to equity are often seen as more stable.


## 2. Sentiment analysis of the company the competitors:
    
    Sentiment analysis is conducted based on the "Competition" section in the SEC 10-K Filling. 

    The sentiment analysis of the company for competitors is useful for investors because - 
    Sentiment analysis can reveal how a company perceives its position relative to competitors and its strategy for maintaining 
    or improving that position. Positive sentiment might indicate confidence in competitive advantages, while negative 
    sentiment could signal challenges or threats.

## Tech Stack used for web-app:
    1. Streamlit
    2. Python

    Why Streamlit?
    Streamlit is designed for Python, making it easy to connect with data tools and add interactive features like sliders and 
    buttons. It works well with popular charting libraries like Matplotlib, Altair, and Plotly, allowing you to create and show 
    detailed graphs quickly. 

## Instructions on how to run the file:
    1. The app is deployed on web server. Please click on this link - https://sec10-k-fillings-analysis.streamlit.app/ to access 
    the web-app. Also, do note that the web-app might take few seconds (30-40 sec) of delay when loading up for the first time. 
    Also, the computations on web-app takes more time as compared to local because of the constraints of the server. This web- 
    app might face issues while loading up since its using a free service and has constraints on memory usage and timeout. 
    Hence, a recording of the app has also been attached in the repo. 

    2. When running from terminal (on local), please execute command (where the project folder is located) - streamlit run 
    app.py

    3. Note, the fillings are already a part of the project since the app is deployed on server and having the fillings helps in 
    avoiding potential delays (since its a free server with constraints on memory and delays). A script is already written to 
    download these files automatically. In app.py inside main() function line 152, the lines are commented. Can uncomment to 
    download the fillings before the execution.


Please do note that, that computations for Debt to Equity ratio analysis and Sentiment analysis might take some time as 
well because the data is huge and process is made to sleep in between while making API calls because of the Rate limiter    
issue of the API (together.ai).

Please note that multiple runs of sentiment analysis might predict different scores and these scores shouldn't be  
treated as baseline facts. They are used as supplemental information to gain better insights from the data.






