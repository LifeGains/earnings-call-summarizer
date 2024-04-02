import requests
import os
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from googleapiclient.discovery import build
import pprint
from datetime import datetime
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Path
dotenv_path = 'C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys\\.env'
load_dotenv(dotenv_path)

def get_text(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    # Pretty print things inside div container.
    # print(soup.find('div').prettify())


    # Find the div with class "article-body"
    article_body = soup.find('div', class_='article-body')

    # Check if the div exists to avoid AttributeError
    if article_body:
        # Get the text within this div, stripping whitespace
        # text = article_body.get_text(strip=True)
        # Get the text within this div
        text = article_body.get_text()
        # Replace each newline character with a space
        text = text.replace('\n', ' ')
        return text
    else:

        # Set up Chrome options
        # chrome_options = Options()
        # chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        # chrome_options.add_argument("--headless")  # Ensure GUI is off
        # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Selenium driver that opens a window
        driver = webdriver.Chrome()
        # Headless Selenium will set off all kinds of alarms.
        # driver = webdriver.Chrome(options=chrome_options)

        # Go to the webpage
        driver.get(url)

        try:
            # Use WebDriverWait to wait for a specific element for up to 10 seconds
            # element_present = EC.presence_of_element_located((By.CLASS_NAME, 'T2G6W'))
            # WebDriverWait(driver, 10).until(element_present)

            # Find the element using the class name
            article_body = driver.find_element(By.CLASS_NAME, 'T2G6W')
            
            # Get the text within this div
            text = article_body.text
            
            # Replace each newline character with a space
            text = text.replace('\n', ' ')

            total_word_count = len(text.split())
            if total_word_count < 1000:
                raise ValueError("Less than 1000 words detected. This means the data is behind a paywall for this quarter/year.\n:("
                 "\nPlease choose another quarter and year combination.")
            else:
                return text

        except TimeoutException:
            # If the element is not found within the given time, TimeoutException will be raised
            return "Timeout waiting for the page to load."

        finally:
            # Close the browser window
            driver.quit()


# Save text to a .txt file
def save_text(text, url):
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Extract the file name from the URL
    file_name = url.rstrip('/').split('/')[-1] + '.txt'
    
    # Construct the full file path
    file_path = os.path.join(current_directory, file_name)
    
    # Writing the text to a file at the specified path
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"File saved to {file_path}")
    return file_path

def summarize_file(file_path):
    # Load your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Initialize client with organization
    client = OpenAI(api_key=openai_api_key
                    , organization='org-DYJXHbCMXBmANo0C18KTFtBk')
    
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Use the OpenAI API to summarize the content
    response = client.chat.completions.create(
    # response = openai.Completion.create(
        model="gpt-3.5-turbo", # Or whichever is the latest version
        messages=[
            {"role": "user", "content": "Summarize the following text into 5 bullet points:\n" + file_content}
        ],
        # max_tokens=150,  # Adjust based on your needs
        # temperature=0.5,  # Adjust for creativity; lower values are more direct
    )
    
    # Extract the text from the response object
    summary = response.choices[0].message.content
    
    return summary

def summarize_directly_from_text_variable(text):
    # Load your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Initialize client with organization
    client = OpenAI(api_key=openai_api_key
                    , organization='org-DYJXHbCMXBmANo0C18KTFtBk')
    
    # Use the OpenAI API to summarize the content
    response = client.chat.completions.create(
    # response = openai.Completion.create(
        model="gpt-3.5-turbo", # Or whichever is the latest version
        messages=[
            {"role": "user", "content": "Summarize the following text into 5 bullet points for an Executive Summary Section, 3 bullet points for a Positive Highlights section, and 3 bullet points for a Negative Highlights section. Use as many numbers and percentages in the summaries as possible:\n" + text}
        ],
        # max_tokens=150,  # Adjust based on your needs
        # temperature=0.5,  # Adjust for creativity; lower values are more direct
    )
    
    # Extract the text from the response object
    summary = response.choices[0].message.content
    
    return summary

def get_url_from_google(quarter, year, company):
    # Source: https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
    # Metrics Google Search API here:
    # https://console.cloud.google.com/apis/api/customsearch.googleapis.com/metrics?project=beaming-grid-374400
    google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    cx = 'd3f4a5934e51b4cc2'
    # cx = 'b48bee4254e8e4b2b' # fool only

    # Keep this in case you want to not only have it be results from fool.com
    # results = google_search(
    #     'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)
    # for result in results:
    #     pprint.pprint(result)
    
    search_query = f"{quarter} + ' ' + {year} + ' ' + {company} + ' earnings call transcript'"

    service = build("customsearch", "v1", developerKey=google_api_key)
    res = service.cse().list(q=search_query, cx=cx).execute()
    # Print the first result
    return res['items'][0]['link']

# results = get_url_from_google('Q1', '2012', 'costco')
# print(get_text(results))

# For streamlit
def app():
    st.title("Earnings Call Summarizer")
    st.caption("Give us any company, along with which quarter and year, and we will give you a 5 bullet point summary of the earnings call.")
    # v1: Fool.com links only.
    # v2: insert Co name, Quarter, and Year only and we will find it automatically.
    with st.form(key='my_form'):
        company_name = st.text_input(
            "Enter the public company name you want to find earnings call transcripts for"
            ,type="default"
            ,placeholder="Eg. Apple, Tesla, Costco, Nvidia, Gamestop"
        )
        quarter_options = ["Q1", "Q2", "Q3", "Q4"]
        quarter_type = st.selectbox("Choose a quarter", quarter_options, index=3)

        year_desc = np.arange(datetime.now().year, 2009, -1)
        year_options = year_desc
        year_type = st.selectbox('Choose a year'
                                    ,year_options
                                    ,index=1)
        
        if st.form_submit_button("Submit"):
            with st.spinner('Generating bullet point summary...'):
                url_name = get_url_from_google(quarter_type, year_type, company_name)
                st.write("URL found: " + url_name)
                st.write("If there is a pop-up, **it will automatically close**. We need it to simulate human behavior.")
                text = get_text(url_name)
                # Print the total word count:
                st.write("Summarizing " + str(len(text.split())) + " words...")
                summary = summarize_directly_from_text_variable(text[100:16000])
                # print(summary)
                return st.markdown(
                    f'''
                    {summary}                   
                    '''
                )

# Only run this if its ran as a standalone program.
if __name__ == '__main__':
    app()