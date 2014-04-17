#!/usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import sqlite3 as lite
import os

CON = None

def connect():
    global CON
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db")
    CON = lite.connect(os.path.join(db_dir, "spiderwave.db"))

def disconnect():
    CON.commit()
    CON.close()

def insert_country(name):
    cur = CON.cursor()

    cur.execute('SELECT * FROM country WHERE name="{cn}"'.format(cn=name))
    country = cur.fetchone()
    if country:
        return country[0]
    cur.execute('INSERT INTO country ( name ) VALUES ("{cn}")'.format(cn=name))
    CON.commit()

    cur.execute('SELECT * FROM country WHERE name="{cn}"'.format(cn=name))
    return cur.fetchone()[0]

def insert_city(name, country_id):
    cur = CON.cursor()

    cur.execute('SELECT * FROM city WHERE name="{cn}" and \
                country_id="{cnt}"'.format(cn=name, cnt=country_id))
    city = cur.fetchone()
    if city:
        return city[0]
    cur.execute('INSERT INTO city ( name, country_id )VALUES ("{cn}", {cnt})'\
                .format(cn=name, cnt=country_id))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM city WHERE name="{cn}" and country_id="{cnt}"'\
                .format(cn=name, cnt=country_id))
    return cur.fetchone()[0]

def insert_streamurl(url, bitrate=0, codec=0, valid=0):
    cur = CON.cursor()

    cur.execute('SELECT * FROM stream_url WHERE url="{u}"'.format(u=url))
    link = cur.fetchone()
    if link:
        return link[0]
    cur.execute('INSERT INTO stream_url ( url, bitrate, format, valid ) VALUES\
            ("{u}", {b}, "{f}", {v})'\
            .format(u=url, b=bitrate, f=codec, v=valid))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM stream_url WHERE url="{u}"'.format(u=url))
    return cur.fetchone()[0]

def insert_genre(name):
    cur = CON.cursor()

    name = BeautifulSoup(unicode(name.strip()).encode('utf-8'), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    try:
        name = unicode(name).encode('utf-8')
    except UnicodeDecodeError:
        name = unicode(name.decode('utf-8')).encode('utf-8')

    cur.execute('SELECT * FROM genre WHERE name="{g}"'.format(g=name))
    genre = cur.fetchone()
    if genre:
        return genre[0]
    cur.execute('INSERT INTO genre ( name ) VALUES ("{g}")'.format(g=name))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM genre WHERE name="{g}"'.format(g=name))
    return cur.fetchone()[0]

def insert_joingenre(radio_id, genre_id):
    cur = CON.cursor()

    cur.execute('SELECT * FROM joingenre WHERE radio_id="{ri}" and \
            genre_id="{gi}"'.format(ri=radio_id, gi=genre_id))
    genre = cur.fetchone()
    if genre:
        return genre[0]
    cur.execute('INSERT INTO joingenre ( radio_id, genre_id ) VALUES ("{ri}",\
            "{gi}")'.format(ri=radio_id, gi=genre_id))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM joingenre WHERE radio_id="{ri}" and \
            genre_id="{gi}"'.format(ri=radio_id, gi=genre_id))
    return cur.fetchone()[0]

def insert_joinstreamurl(radio_id, stream_url_id):
    cur = CON.cursor()

    cur.execute('SELECT * FROM joinstreamurl WHERE radio_id="{ri}" and \
            stream_url_id="{sui}"'.format(ri=radio_id, sui=stream_url_id))
    genre = cur.fetchone()
    if genre:
        return genre[0]
    cur.execute('INSERT INTO joinstreamurl ( radio_id, stream_url_id ) VALUES \
            ("{ri}", "{sui}")'.format(ri=radio_id, sui=stream_url_id))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM joinstreamurl WHERE radio_id="{ri}" and \
            stream_url_id="{sui}"'.format(ri=radio_id, sui=stream_url_id))
    return cur.fetchone()[0]

def insert_radio(name, city_id, homepage, logo, web_only):
    cur = CON.cursor()

    cur.execute('SELECT * FROM radio WHERE name="{n}" and \
            city_id="{ci}"'.format(n=name, ci=city_id))
    genre = cur.fetchone()
    if genre:
        return genre[0]
    cur.execute('INSERT INTO radio ( name, logo, homepage, city_id, webonly ) \
            VALUES ("{n}", "{l}", "{h}", "{ci}", "{w}")'.format(n=name, l=logo,
                h=homepage, ci=city_id, w=web_only))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM radio WHERE name="{n}" and \
            city_id="{ci}"'.format(n=name, ci=city_id))
    return cur.fetchone()[0]

def add_radio(name, city, country, stream_urls, genres, logo=None,
        homepage=None, web_only=0):

    # Sanitize everything
    name = BeautifulSoup(unicode(name.strip()).encode('utf-8'), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    try:
        name = unicode(name).encode('utf-8')
    except UnicodeDecodeError:
        name = unicode(name.decode('utf-8')).encode('utf-8')

    city = BeautifulSoup(unicode(city.strip()).encode('utf-8'), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    try:
        city = unicode(city).encode('utf-8')
    except UnicodeDecodeError:
        city = unicode(city.decode('utf-8')).encode('utf-8')

    country = BeautifulSoup(unicode(country.strip()).encode('utf-8'), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    try:
        country = unicode(country).encode('utf-8')
    except UnicodeDecodeError:
        city = unicode(country.decode('utf-8')).encode('utf-8')

    #Get country id
    country_id = insert_country(country)

    #Get city id
    city_id = insert_city(city, country_id)

    stream_url_ids = []
    #Get stream_url ids
    for stream_url, br in stream_urls:
        stream_url_ids.append(insert_streamurl(stream_url, bitrate=br))

    genre_ids = []
    #Get genres ids
    for genre in genres:
        genre_ids.append(insert_genre(genre))

    #Get radio id
    radio_id = insert_radio(name, city_id, homepage, logo, web_only)

    #update joingenre
    for genre_id in genre_ids:
        insert_joingenre(radio_id, genre_id)

    #update joinstream
    for stream_url_id in stream_url_ids:
        insert_joinstreamurl(radio_id, stream_url_id)

    return

