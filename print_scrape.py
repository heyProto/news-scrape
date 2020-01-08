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
wks = gc.open("Scraped articles").sheet3
"""

# change loop numbers to scrape more
urlBegin = 'https://theprint.in/category/india/page/'
a = int(input("Start from page: "))
b = int(input("End at page: "))
with open('print_india_articles.csv', mode='a') as news_file:
    news_writer = csv.writer(news_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(a, b):
        print "scraping page", str(i)
        url = urlBegin + str(i)
        r = urllib.urlopen(url).read()
        soup= BeautifulSoup(r, "html.parser")
        links = [a['href'] for a in soup.select('.td-read-more a')]
        for link in links:
            request_href = requests.get(link)
            soup2 = BeautifulSoup(request_href.content, "html.parser")
            if len(soup2.select('.td-post-source-tags a')) != 0:
                tags = ', '.join([str(a.text) for a in soup2.select('.td-post-source-tags a')])
            else:
                tags = ""

            author = soup2.select('.author')[0].text

            date = soup2.select('.update_date')[0].text

            title = soup2.select('h1.entry-title')[0].text

            
            news_writer.writerow([title, date, author, tags, link])
            # wks.append_row([title, date, author, tags, link])


