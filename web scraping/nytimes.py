from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import csv
import os

def scrape_news(date):
    file_path = 'news_article.csv'
    
    # Open the file and write the header if the file is empty
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.stat(file_path).st_size == 0:
            writer.writerow(['News_Description'])
    
    # Format the URL with the current date
    date_str = date.strftime('%Y/%m/%d')
    url = f"https://www.nytimes.com/issue/todayspaper/{date_str}/todays-new-york-times"
    
    try:
        # Make a GET request to fetch the raw HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        html_text = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_text, 'lxml')
        # Adjust the class name according to the current NYTimes structure
        news = soup.find_all('p', class_='css-tskdi9')
        
        # Open the CSV file once outside the loop
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Loop through the news paragraphs and write them to the CSV file
            for new in news:
                news_description = new.text.strip()
                writer.writerow([news_description])
                print(f"news_description : {news_description}\n")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2021, 6, 10)
    delta = timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        scrape_news(current_date)
        current_date += delta
