# Earnings Call Transcript Finder and Summarizer

### App is located here: https://earnings-call-summarizer.streamlit.app/

# Description

Given the company, quarter, and year, automatically finds the earnings call transcript and create a 5 bullet executive summary of the earnings call transcript. In addition, also produces a 3 bullet point "Pros" and "Cons" list.

# Jira To Do Nexts / Blockers

- Full, Free Earnings transcript texts are only reliably found >= 2018. 
    - Seekingalpha is unable to work with BeautifulSoup or Non-headless Selenium. 
    - Figure out a way around this.
- Quality / detailedness of earnings summary can be improved and/or tailored for financial analysts and what they find important.
- Add Gumroad/Stripe checkout

# Stack

- Python
- Google Custom Search API
- Openai API
- Streamlit
- Gumroad/Stripe (TBD)