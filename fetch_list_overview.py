#!/usr/bin/python

import bs4 as BeautifulSoup
import requests

import db_wrapper

BASE_URL = "http://www.icheckmovies.com"
LIST_PATH = "/lists/"

def fetch_list_and_add(db, base_path, start_url):
    r = requests.get(start_url)
    soup = BeautifulSoup.BeautifulSoup(r.text)

    db.set_update_sql("lists", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)")
    db.set_update_sql("list_tags", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, CURRENT_TIMESTAMP)")
    db.set_update_sql("list_progress", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, ?, CURRENT_TIMESTAMP)")

    for item in soup.find_all('li', attrs={'class': 'listItemToplist'}):
        link = item.find('a', attrs={'class': 'title'})

        if link is None:
            print "Could not find link with class 'title', skipping"
            continue

        href = link['href']
        name = link.find('span').contents[0]
        favs_dislikes = item.find('strong').contents[0].split(':')
        description_tag = item.find('span', attrs={'class': 'infoListDescription'})

        # Description does not always exist
        if len(description_tag.contents) > 0:
            # TODO: Better strategy for handling problematic characters
            description = description_tag.contents[0].encode('utf-8', 'ignore')
        else:
            description = None

        tags = []
        for tag in item.find_all('a', attrs={'class': 'tagNamespaceCategory'}):
            tags.append(tag.contents[0])

        user = item.find('a', attrs={'class': 'tagNamespaceUser'}).contents[0]

        db.update_db("lists", [href, name, None, favs_dislikes[0], favs_dislikes[1], str(description), user])

        # Purge the old tags and include the active list of tags
        db.get_cursor().execute("DELETE FROM list_tags WHERE list_link=?", (href,))
        for tag in tags:
            db.update_db("list_tags", [href, tag])

    next_link = soup.find('li', attrs={'class': 'next'}).find('a')
    if next_link is not None:
        fetch_list_and_add(db, base_path + next_link['href'])

    #db.print_db("lists")
    #db.print_db("list_tags")

db = db_wrapper.db_wrapper(name="icheckmovies.db")
fetch_list_and_add(db, base_path=BASE_URL + LIST_PATH, start_url=BASE_URL + LIST_PATH + "?tags=user:icheckmovies")
