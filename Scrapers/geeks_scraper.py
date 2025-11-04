# scrapers/geeks_scraper.py
import requests
from bs4 import BeautifulSoup
from models import get_session, Question


html_text =  requests.get('https://www.geeksforgeeks.org/software-engineering/software-engineering-interview-questions-and-answers/').text

soup = BeautifulSoup(html_text, 'lxml')
div = soup.find('div', class_ = 'text')
questions = div.find_all('h3')

for question in questions:
    print(question.text)
#
   