from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import os

def scrape_news():

    with open('news_article.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if os.stat('news_article.csv').st_size == 0:
            writer.writerow(['News_Description'])


    web_link=input("Enter the link of the website: ")
    html_text=requests.get(web_link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('span', class_='container__headline-text')
    for new in news:
        news_description = new.text
        

        with open('news_article.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([news_description])
        print (f"news_description : {news_description.strip()}\n")


if __name__ == '__main__':
    while(True):
        scrape_news()