#!/usr/bin/python

import bs4 as BeautifulSoup
import requests
import re
import time

import db_wrapper

BASE_URL = "http://www.icheckmovies.com"

def import_one_list(db, base_url, list_link):
    r = requests.get(BASE_URL + list_link)
    soup = BeautifulSoup.BeautifulSoup(r.text)
    #with open('top250.html', 'r') as fh:
    #    text = fh.read()
    #soup = BeautifulSoup.BeautifulSoup(text)

    count = 0

    for item in soup.find_all('li', attrs={'class': 'listItemMovie'}):
        count = count + 1
        link = item.find('a', attrs={'class': 'dvdCoverSmall'})

        if link is None:
            print "Could not find a link with class 'dvdCoverSmall', skipping"
            continue

        href = link['href']

        match = re.search(r'View detailed information on (.*) \((\d+)\)', link['title'])
        if match is not None:
            title = match.group(1)
            year = match.group(2)
        else:
            print "Could not isolate title and year for film with link {}, skipping".format(link)
            continue

        # There's not a clear ID for the top lists count, so isolate links
        # and accept the first one that matches
        top_lists = None
        info_subset = item.find('span', attrs={'class': 'info'})
        for a_subset in info_subset.find_all('a'):
            # Note that it can be either 'list' or 'lists'
            match = re.search(r'(\d+) top list', a_subset.contents[0])
            if match is not None:
                top_lists = match.group(1)
                break

        tags = []
        tag_subset = item.find('ul', attrs={'class': 'tagList'})
        # The tags have no class, except for the type, user, and year
        for tag in tag_subset.find_all('a', attrs={'class': ''}):
            tags.append(tag.contents[0])

        user_subset = tag_subset.find('a', attrs={'class': 'tagNamespaceUser'})
        if user_subset is not None:
            user = user_subset.contents[0]
        else:
            user = None

        db.update_db("films", [href, title, year, top_lists, user])

        # Purge the old tags and include the active list of tags
        db.get_cursor().execute("DELETE FROM film_tags WHERE film_link=?", (href,))
        for tag in tags:
            db.update_db("film_tags", [href, tag])

        db.update_db("list_items", [list_link, href])

        print "Added {0}:{1}:{2}:{3}:{4}:{5}:{6}".format(list_link, href, title.encode('utf-8', 'ignore'), year, top_lists, tags, user)

    if count > 0:
        db.get_cursor().execute("UPDATE lists SET size=? WHERE list_link=?", (count, list_link))

def import_all(db_file):
    db = db_wrapper.db_wrapper(name=db_file)

    db.set_update_sql("films", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)")
    db.set_update_sql("film_tags", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, CURRENT_TIMESTAMP)")
    db.set_update_sql("film_progress", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, ?, CURRENT_TIMESTAMP)")
    db.set_update_sql("list_items", "INSERT OR REPLACE INTO {0} VALUES(NULL, ?, ?, CURRENT_TIMESTAMP)")

#    import_one_list(db, BASE_URL, "/lists/top+250/")
#    import_one_list(db, BASE_URL "/lists/the+criterion+collection/")
#    quit()
    for item in db.get_cursor().execute("SELECT * FROM lists").fetchall():
        import_one_list(db, BASE_URL item[1])
        time.sleep(1)
    db.close_db()

import_all("icheckmovies.db")
