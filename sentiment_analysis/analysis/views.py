from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Search
from django.db.models import Sum
import pandas as pd
from .text_preprocessing import clean_text
from .nlp import get_sentiment
from .visualisation import get_pie_chart, get_line_chart, get_word_cloud, get_multiple_pie_charts
import os

def HomePage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    users = User.objects.all()
    num_users = len(users)
    all_searches = Search.objects.all()
    num_searches = sum([search.count for search in all_searches])
    top_searches = (Search.objects
                    .values('keyword')
                    .annotate(total_count=Sum('count'))
                    .order_by('-total_count')[:10])


    if request.method == 'POST':
        last_submission_time = cache.get('last_submission_time')
        if last_submission_time is None or datetime.now() - last_submission_time > timedelta(seconds=30):
            search_keyword = request.POST.get('keywords', None)
            search_keyword = search_keyword.lower()
            if search_keyword:

                existing_search = Search.objects.filter(keyword=search_keyword,user=None).first()

                if existing_search:
                    existing_search.created_at = datetime.now()
                    existing_search.count += 1
                    existing_search.save()
                else:
                    new_search = Search(keyword=search_keyword,user=None,created_at=datetime.now())
                    new_search.save()

                top_searches = (Search.objects
                    .values('keyword')
                    .annotate(total_count=Sum('count'))
                    .order_by('-total_count')[:10])

                all_searches = Search.objects.all()
                num_searches = sum([search.count for search in all_searches])
               
                newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))
                all_articles = newsapi.get_everything(q=search_keyword, language='en', sort_by='relevancy')
                articles = all_articles.get('articles', [])

                articles_data = []
                for article in articles:
                    source = article.get('source', {}).get('name', '')
                    description = article.get('description', '')
                    url = article.get('url', '')
                    image_url = article.get('urlToImage', '')

                    if description is not None and url is not None:
                        article_data = {
                            'source': source,
                            'description': description,
                            'url': url,
                            'image_url': image_url
                        }

                        articles_data.append(article_data)

                # print('\n')
                # print(articles_data)
                # print('\n')
                # print(len(articles_data))

                if len(articles_data) == 0:
                    messages.error(request, 'No news articles found for the given search query. Please try again with a different search query.')
                    return render(request, 'home.html', {'num_users': num_users, 'num_searches': num_searches, 'top_searches': top_searches})


                cache.set('last_submission_time', datetime.now(), 30)
                return render(request, 'home.html', {'articles_data': articles_data, 'num_users': num_users, 'num_searches': num_searches, 'top_searches': top_searches})


        else:
            messages.error(request, 'Please wait for 30 seconds before submitting another search query.')
            return render(request, 'home.html', {'num_users': num_users, 'num_searches': num_searches, 'top_searches': top_searches})
    
    return render(request, 'home.html', {'num_users': num_users, 'num_searches': num_searches, 'top_searches': top_searches})





@login_required(login_url='login')
def DashboardPage(request):
    user=request.user
    # recent searches of this user
    recent_searches = Search.objects.filter(user=user).order_by('-created_at')[:10]
    top_searches = (Search.objects
                    .values('keyword')
                    .annotate(total_count=Sum('count'))
                    .order_by('-total_count')[:10])

    if request.method == 'POST':
        last_submission_time = cache.get('last_submission_time')
        if last_submission_time is None or datetime.now() - last_submission_time > timedelta(seconds=30):
            search_keyword = request.POST.get('keywords', None)
            search_keyword = search_keyword.lower()
            if search_keyword:

                existing_search = Search.objects.filter(keyword=search_keyword,user=user).first()

                if existing_search:
                    existing_search.created_at = datetime.now()
                    existing_search.count += 1
                    existing_search.save()
                else:
                    new_search = Search(keyword=search_keyword, user=user,created_at=datetime.now())
                    new_search.save()

                recent_searches = Search.objects.filter(user=user).order_by('-created_at')[:10]
                top_searches = (Search.objects
                    .values('keyword')
                    .annotate(total_count=Sum('count'))
                    .order_by('-total_count')[:10])

                newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))
                all_articles = newsapi.get_everything(q=search_keyword, language='en', sort_by='relevancy')
                articles = all_articles.get('articles', [])

                articles_data = []
                for article in articles:
                    source = article.get('source', {}).get('name', '')
                    description = article.get('description', '')
                    url = article.get('url', '')
                    image_url = article.get('urlToImage', '')
                    publish_date = article.get('publishedAt', '')

                    if description is not None and url is not None:
                        article_data = {
                            'source': source,
                            'description': description,
                            'url': url,
                            'image_url': image_url,
                            'publish_date': publish_date
                        }

                        articles_data.append(article_data)

                if len(articles_data) == 0:
                    messages.error(request, 'No news articles found for the given search query. Please try again with a different search query.')
                    return render(request, 'dashboard.html', {'user': user, 'recent_searches': recent_searches,
                                     'top_searches': top_searches})


                df = pd.DataFrame(articles_data)
                df = clean_text(df)
                df = get_sentiment(df)
                pie_chart = get_pie_chart(df)
                line_chart=get_line_chart(df)
                word_cloud=get_word_cloud(df)
                multiple_pie_chart=get_multiple_pie_charts(df)


                articles_data = df.to_dict('records')
                num_pos_news=len(df[df['label']=='positive'])
                num_neg_news=len(df[df['label']=='negative'])
                num_neu_news=len(df[df['label']=='neutral'])

                cache.set('last_submission_time', datetime.now(), 30)
                return render(request, 'dashboard.html', {'user': user, 'recent_searches': recent_searches,
                                     'articles_data': articles_data,'top_searches': top_searches,
                                     'num_pos_news':num_pos_news,'num_neg_news':num_neg_news,'num_neu_news':num_neu_news,
                                     'pie_chart':pie_chart,'line_chart':line_chart,'word_cloud':word_cloud,
                                     'multiple_pie_chart':multiple_pie_chart})


        else:
            messages.error(request, 'Please wait for 30 seconds before submitting another search query.')
            return render(request, 'dashboard.html', {'user': user, 'recent_searches': recent_searches,'top_searches': top_searches})

    

    return render(request, 'dashboard.html', {'user': user, 'recent_searches': recent_searches,'top_searches': top_searches})

def AboutPage(request):
    return render(request, 'about.html')
