#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import subprocess
import re
import sys
import urllib2

import db_wrapper

def get_page( url ):
    opener = urllib2.build_opener()
    data = opener.open(url).read()
    soup = BeautifulSoup(data)
    return soup

db_wrapper.connect()
cnt_id = db_wrapper.insert_country("United States")

soup = get_page("http://www.usliveradio.com/")
radios = soup.find("table", {"id" : "thetable3"})
for row in radios.findAll('tr'):
    if len(row.findAll('th')) > 0:
        continue
    name_link = row.findAll('td')[0].findAll('a')
    if len(name_link) > 0:
        name = name_link[0].text
        url = name_link[0]['href']

    city = row.findAll('td')[1].text
    state = row.findAll('td')[2].text
    location = "%s;%s" % (city, state)

    stream_href = row.findAll('td')[4].findAll('a')[0]
    stream = stream_href["href"]
    if "javascript:" in stream:
        open_js = stream[stream.find("(")+1:stream.find(")")]
        open_arg = open_js[open_js.find("(")+1:open_js.find(")")]
        args = open_arg.split(',')
        stream = args[0].strip('\'')
    quality = stream_href.link

    categ = []
    if len(row.findAll('td')) > 5:
        categ = row.findAll('td')[5].text
        categ = re.split(', |/', categ)

    # Insert a City of a country
    city_id = db_wrapper.insert_city(location, cnt_id)
    # Insert the genre
    genres_id = []
    for cat in categ:
        genres_id.append(db_wrapper.insert_genre(cat))

    # TODO: Handle multiple stream URLs
    stream_id = [db_wrapper.insert_streamurl(stream)]

    # Finally, the whole radio
    db_wrapper.insert_radio(name, stream_url_ids=stream_id, genre_ids=genres_id, country_id=cnt_id, city_id=city_id, homepage=url)

    print '-'*80
    print name
    print url
    print location
    print stream
    print categ

db_wrapper.disconnect()
