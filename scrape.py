import urllib
from bs4 import *
import re
# import gspread
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('News Scraping-b8147747a15e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Scraped articles").sheet1
"""

# change loop numbers to scrape more
urlBegin = 'https://indianexpress.com/latest-news/'
a = int(input("Start from page: "))
b = int(input("End at page: "))
with open('news_articles.csv', mode='w') as news_file:
    news_writer = csv.writer(news_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(a, b):
        print "scraping page", str(i)
        url = urlBegin + str(i)
        r = urllib.urlopen(url).read()
        soup= BeautifulSoup(r, "html.parser")
        links = [a['href'] for a in soup.select('.title a[href]')]
        for link in links:
            request_href = requests.get(link)
            soup2 = BeautifulSoup(request_href.content, "html.parser")
            if len(soup2.select('.storytags a')) != 0:
                tags = ', '.join([str(a.text) for a in soup2.select('.storytags a')])
            else:
                tags = ""

            if len(soup2.select('.editor a')) != 0:
                author = soup2.select('.editor a')[0].text
            elif len(soup2.select('.editorbx a')) != 0:
                author = soup2.select('.editorbx a')[0].text
            else:
                author = ""

            if len(soup2.select('.editor span[itemProp = "dateModified"]')) != 0:
                date = soup2.select('.editor span[itemProp = "dateModified"]')[0]['content']
            elif len(soup2.select('.editorbx span')) != 0:
                date = soup2.select('.editorbx span')[0]['content']
            else:
                date = ""

            if len(soup2.select('.native_story_title')) != 0:
                title = soup2.select('.native_story_title')[0].text
            elif len(soup2.select('.heading-part h1')) != 0:
                title = soup2.select('.heading-part h1')[0].text
            else:
                title = ""

            
            news_writer.writerow([title, date, author, tags, link])
            # wks.append_row([title, date, author, tags, link])


