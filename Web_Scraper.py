# find libraries for web scraping

import requests
import re
from bs4 import BeautifulSoup as Bs
import time
import datetime
import sqlite3

database = 'breitbart.db'

url = 'http://www.breitbart.com'



words_ = ["Obama", "Trump", "ISIS", "hoax", "media", "guns", "russia", "Putin", 'extremist', "God"]

conn = sqlite3.connect(database)

# define cursor

c = conn.cursor()

def create_table(words_):
    c.execute("CREATE TABLE IF NOT EXISTS breitbartData(Date, %s)" % ", ".join(words_)) 

def get_request(url):
    page = requests.get(url)
    content = page.content
    soup = Bs(content, 'html.parser')
    return soup


sopa = get_request(url)

# create article list
# find all 'article' html tags; add each tag to article_list

article_list = [tag for tag in sopa.find_all("article")]

# create 'links' list
# find all 'href' url's in list of article tags; add each url to 'links'

def create_hreflist():
    links = []
    for article in article_list:
        hrefs = article.a.get('href')
        links.append(hrefs)
    return links


href_list = create_hreflist()

# combine main url with href directory
def create_url(href_list):
    new_pages = []
    for link in href_list:
        new_url = url + link
        new_pages.append(new_url)
    return new_pages

art_pages = create_url(href_list)

print(enumerate(art_pages))
print("-----")
print(len(art_pages))


def main(art_pages, words_):

    amnt_list = []
    i = 0
    daily_amnt = 0

    # iterate process for each word in words_
    for x in range(len(words_)):

        for page in art_pages:
            page_req = requests.get(page)
            print("--Sending Request--")
            get_content = page_req.content
            # create soup object
            new_soup = Bs(get_content, 'html.parser')
            # find all paragraph tags on page
            para_tags = (new_soup.find_all('p'))
            # convert paragraph tags to strings
            str_para = str(para_tags)
            # parse page for word
            found_on_page = re.findall(words_[x], str_para)
            i += 1
            print("Times word '{}' was found on page {}: {}".format(words_[x], i, len(found_on_page)))

            daily_amnt += len(found_on_page)

        print("The word {} was mentioned {} times today on {}".format(words_[x], daily_amnt, url))
        amnt_list.append(daily_amnt)
        # return daily_amnt
        print("\n")
        print("======")
        daily_amnt = 0
        i = 0
    return amnt_list



def dynamic_data_entry(amnts):
    today = str(datetime.date.today())
    our_amounts = amnts
    c.execute("INSERT INTO breitbartData VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (today, *our_amounts))
    conn.commit()
# a sum changes everytime a loop iterates. return the sum every iteration and store it in the coresponding column in the database. 


create_table(words_)
print("----")

main_func = main(art_pages, words_)
dynamic_data_entry(main_func)

c.close()
conn.close()
# per each request, parse the page with all five words


# Begin to implement SQL.
# store word count in database based on date
# create record for every day, and columns per word
# update the database daily
# have the script run daily without me having to run it
# run every day




