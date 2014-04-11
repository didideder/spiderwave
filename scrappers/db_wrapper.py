#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import os

CON = None

def connect():
    global CON
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db")
    CON = lite.connect(os.path.join(db_dir, "spiderwave.db"))

def disconnect():
    global CON
    CON.commit()
    CON.close()

def insert_country(name):
    global CON
    cur = CON.cursor()

    name = unicode(name).encode('utf-8')

    cur.execute('SELECT * FROM country WHERE name="{cnt}"'.format(cnt=name))
    country = cur.fetchone()
    if country:
        return country[0]
    cur.execute('INSERT INTO country (name) VALUES ("{cnt}")'.format(cnt=name))
    CON.commit()

    cur.execute('SELECT * FROM country WHERE name="{cnt}"'.format(cnt=name))
    return cur.fetchone()[0]

def insert_city(name, country):
    global CON
    cur = CON.cursor()

    name = unicode(name).encode('utf-8')

    cur.execute('SELECT * FROM city WHERE name="{cn}" and country_id="{cnt}"'.format(cn=name, cnt=country))
    city = cur.fetchone()
    if city:
        return city[0]
    cur.execute('INSERT INTO city (name, country_id) VALUES ("{cn}", {cnt})'.\
                        format(cn=name, cnt=country))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM city WHERE name="{cn}" and country_id="{cnt}"'.format(cn=name, cnt=country))
    return cur.fetchone()[0]

def insert_genre(name):
    global CON
    cur = CON.cursor()

    name = unicode(name).encode('utf-8')

    cur.execute('SELECT * FROM genre WHERE name="{gn}"'.format(gn=name))
    genre = cur.fetchone()
    if genre:
        return genre[0]
    cur.execute('INSERT INTO genre (name) VALUES ("{gn}")'.format(gn=name))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM genre WHERE name="{gn}"'.format(gn=name))
    return cur.fetchone()[0]

def insert_streamurl(url, bitrate):
    global CON
    cur = CON.cursor()

    cur.execute('SELECT * FROM stream_url WHERE url="{a}"'.format(a=url))
    link = cur.fetchone()
    if link:
        return link[0]
    cur.execute('INSERT INTO stream_url (url, bitrate) VALUES ("{a}", {b})'.format(a=url, b=bitrate))
    CON.commit()
    # Then grab the ID and return that.
    cur.execute('SELECT * FROM stream_url WHERE url="{a}"'.format(a=url))
    return cur.fetchone()[0]

def insert_radio(name, logo=None, stream_url_ids=None, genre_ids=None, country_id=None, city_id=None, homepage=None, valid=0, web_only=0):
    global CON
    cur = CON.cursor()

    try:
        name = unicode(name).encode('utf-8')
    except UnicodeDecodeError:
        name = unicode(name.decode('utf-8')).encode('utf-8')

    cur.execute('SELECT * FROM radio WHERE name="{n}" and country_id={cnt} and city_id={cid}'.format(n=name, cnt=country_id, cid=city_id))
    radio = cur.fetchone()
    if radio:
        radio_id = radio[0]

        db_stream_url_ids = radio[4].split(';')
        for stream in stream_url_ids:
            if stream not in db_stream_url_ids:
                db_stream_url_ids.append(str(stream))
        db_stream_url_ids = list(set(db_stream_url_ids))
        cur.execute('UPDATE radio SET stream_url_ids="{stream_url}" WHERE id={rd}'.format(stream_url=';'.join(db_stream_url_ids), rd=radio_id))
        CON.commit()

        db_genre_ids = radio[5].split(';')
        for genre in genre_ids:
            if genre not in db_genre_ids:
                db_genre_ids.append(str(genre))
        db_genre_ids = list(set(db_genre_ids))
        cur.execute('UPDATE radio SET genre_ids="{genre}" WHERE id={rd}'.format(genre=';'.join(db_genre_ids), rd=radio_id))
        CON.commit()

        db_homepage = radio[3]
        if homepage is not None and db_homepage is None:
            cur.execute('UPDATE radio SET homepage="{dbh}" WHERE id={rd}'.format(dbh=homepage, rd=radio_id))
            CON.commit()

        return

    stream_url_str = ';'.join(map(str, stream_url_ids))
    genre_str = ';'.join(map(str, genre_ids))
    cur.execute('INSERT INTO radio (name, logo, homepage, stream_url_ids, genre_ids, country_id, city_id, valid, webonly) \
                        VALUES ("{n}", "{l}", "{h}", "{st}", "{g}", {ct}, {c}, 0, 0)'.format(\
                        n=name, l=None, h=homepage, st=stream_url_str, g=genre_str, ct=country_id, c=city_id))
    CON.commit()
    return

