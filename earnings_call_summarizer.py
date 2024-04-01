import requests
import os
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import streamlit as st

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
        return "The specified div class 'article-body' was not found."

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
            {"role": "user", "content": "Summarize the following text into 5 bullet points:\n" + text}
        ],
        # max_tokens=150,  # Adjust based on your needs
        # temperature=0.5,  # Adjust for creativity; lower values are more direct
    )
    
    # Extract the text from the response object
    summary = response.choices[0].message.content
    
    return summary
# print(os.getcwd())
# url = 'https://www.fool.com/earnings/call-transcripts/2024/01/24/tesla-tsla-q4-2023-earnings-call-transcript/'
# text = get_text(url)
# # print(text)
# file_path = save_text(text, url)
# summary = summarize_file(file_path)
# print(summary)

# For streamlit
def app():
    st.title("Earnings Call Summarizer")
    st.caption("Paste in any earnings call transcript from fool.com and we will give you a 5 bullet point summary of it.")
    with st.form(key='my_form'):
        url_name = st.text_input(
            "Enter the URL of earnings transcript from fool.com"
            ,type="default"
            ,placeholder="Eg. https://www.fool.com/earnings/call-transcripts/2024/01/24/tesla-tsla-q4-2023-earnings-call-transcript/"
        )
        if st.form_submit_button("Submit"):
            with st.spinner('Generating bullet point summary...'):
                text = get_text(url_name)
                summary = summarize_directly_from_text_variable(text)
                # print(summary)
                return st.markdown(
                    f'''
                    {summary}                   
                    '''
                )

# Only run this if its ran as a standalone program.
if __name__ == '__main__':
    app()
