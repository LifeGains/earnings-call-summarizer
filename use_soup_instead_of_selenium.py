import requests 

from bs4 import BeautifulSoup as bs 



# load the projectpro webpage content 
url = 'https://seekingalpha.com/article/4029032-costco-wholesale-cost-q1-2017-results-earnings-call-transcript'
# r = requests.get(url)
html = requests.get(url).text
print(html)


# convert to beautiful soup 

# soup = bs(r.content) 



# printing our web page 

# print(soup.prettify()) 