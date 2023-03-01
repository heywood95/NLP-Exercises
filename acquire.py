#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
from requests import get
import os
import pandas as pd
import json


def get_blog_articles(article_list):
    
    file = 'blog_posts.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
        
            return json.load(f)
    
    headers = {'User-Agent': 'Codeup Data Science'}
    
    article_info = []
    
    for article in article_list:
        
        response = get(article, headers=headers)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        info_dict = {'title': soup.find('h1').text,
                     'link': article,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text}
    
        article_info.append(info_dict)
        
    with open(file, 'w') as f:
        
        json.dump(article_info, f)
        
    return article_info
        
        
def scrape_one_page(topic):
    url = 'https://inshorts.com/en/read/'
    response = requests.get(url + topic)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find_all('span', itemprop='headline')
    article = soup.find_all('div', itemprop='articleBody')
    
    summary_list = []

    for i in range(len(title)):
    
        temp_dict = {'category': topic,
                    'title': title[i].text,
                    'content': article[i].text}
        summary_list.append(temp_dict)
    return summary_list


def get_news_articles(topic_list):
    
    file = 'news_articles.json'
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
        
    final_list = []
    
    for topic in topic_list:
        final_list.extend(scrape_one_page(topic))
    with open(file, 'w') as f:
        json.dump(final_list, f)
        
    return final_list

