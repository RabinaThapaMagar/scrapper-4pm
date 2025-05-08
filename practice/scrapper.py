import requests
from bs4 import BeautifulSoup

URL= "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    print(response)

scrape_books(URL)
