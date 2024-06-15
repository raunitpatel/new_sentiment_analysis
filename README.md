
# NewsMood Analyzer

NewsMood is your go-to platform for insightful news sentiment analysis. Whether you're curious about the latest trending topic or want to delve into the emotional landscape of a specific event, we've got you covered. Simply enter a keyword, and our sophisticated sentiment analysis engine will sift through thousands of news articles, bringing you not just the information, but the emotional pulse of the story.
## Key Concepts

- **Django Web App**
  - Developed a web application using Django.
  - Implemented views, templates, and models for data handling.

- **NewsAPI Integration**
  - Used NewsAPI to fetch real-time news articles based on specific queries.
  - Processed JSON responses to extract relevant news data.

- **Web Scraping**
  - Implemented web scraping techniques to gather supplementary news content.
  - Used BeautifulSoup for parsing and extraction.

- **Sentiment Analysis with RoBERTa**
  - Integrated a pretrained RoBERTa model for sentiment analysis.
  - Applied natural language processing techniques to determine sentiment (positive, negative, neutral).

## Technologies Used

- **Backend:** Python, Django
- **API:** NewsAPI
- **Web Scraping Tools:** BeautifulSoup, Scrapy
- **Machine Learning/NLP:** RoBERTa, Hugging Face Transformers

## Project Workflow

1. **Data Collection**
   - Fetching news articles using NewsAPI.
   - Scraping additional content from relevant websites.

2. **Data Processing**
   - Parsing and cleaning data retrieved from NewsAPI and web scraping.

3. **Sentiment Analysis**
   - Applying RoBERTa model to analyze sentiment of news articles.

4. **Presentation**
   - Displaying news articles along with sentiment analysis results on the Django web interface.



## Installation

Python and Django need to be installed

```bash
  pip install -r requirements.txt
```
Go to sentiment_analysis folder
```bash
  python manage.py runserver
```
Then go to the browser and enter the url http://127.0.0.1:8000/

## Login and Signup
Users can register through register page.
Then, user can login through login page.

You can access the django admin page at http://127.0.0.1:8000/admin and login with username 'admin' and password 'admin@123'.

Also a new admin user can be created using
```bash
  python manage.py createsuperuser
```

    
## Screenshots
![Screenshot 2024-06-15 125733](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/28309095-6ff9-4b29-adc1-664bb6f7a7d9)
![Screenshot 2024-06-15 130036](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/d2d97e80-7abe-42ee-a187-7df0899bfc3a)
![Screenshot 2024-06-15 130054](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/2104ff64-e1ba-4ffb-879a-df6cd0038af1)
![Screenshot 2024-06-15 130113](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/931cde54-3a0e-464e-b8d6-16e108993436)
![Screenshot 2024-06-15 125903](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/cf26913e-5e23-4cdf-b057-5dee1968a1e9)
![Screenshot 2024-06-15 125923](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/258b46c0-7bb0-416a-a9e7-a161481d756a)
![Screenshot 2024-06-15 125946](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/64450d56-e07a-4045-a691-557e4f813fa0)
![Screenshot 2024-06-15 130008](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/721dd8c3-95d5-4970-900a-3aa5d02f3f44)
![Screenshot 2024-06-15 133917](https://github.com/raunitpatel/new_sentiment_analysis/assets/118679198/75365443-c10e-4150-9656-8a0a34647473)



