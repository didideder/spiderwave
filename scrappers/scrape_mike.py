#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import db_wrapper

def get_page(url):
    opener = urllib2.build_opener()
    data = opener.open(url).read()
    soup = BeautifulSoup(data)
    return soup

# main_id : dict: {"type": "name"}; Example: {"class":"thetable3"}
def scrape(data, name_td_id=0, location_td_id=1, stream_td_id=3, categ_td_id=4, country=None):
    non_decimal = re.compile(r'[^\d.]+')
    for row in data.findAll('tr'):
        if len(row.findAll('th')) > 0:
            continue
        name_link = row.findAll('td')[name_td_id].findAll('a')
        location = row.findAll('td')[location_td_id].text
        if country == "US" or country.startswith("United States - "):
            state = row.findAll('td')[2].text
            country = "United States - %s" % unicode(state).encode('utf-8')
        if "Location" in location:
            continue
        if len(name_link) > 0:
            name = name_link[0].text
            name = name.replace('"','')
            url = unicode(name_link[0]['href']).encode('utf-8')
        if name == "":
            name = row.findAll('td')[0].findAll('b')[1].text
            if name == "":
                print "Name is empty - %s" % country
                sys.exit(0)

        stream_href_list = row.findAll('td')[stream_td_id].findAll('a')
        streams = []
        for stream_href in stream_href_list:
            stream = stream_href["href"]
            quality = stream_href.text
            try:
                quality = int(non_decimal.sub('', quality))
            except ValueError:
                quality = 0
            if "javascript:" in stream:
                open_js = stream[stream.find("(")+1:stream.find(")")]
                open_arg = open_js[open_js.find("(")+1:open_js.find(")")]
                args = open_arg.split(',')
                stream = args[0].strip('\'')
            streams.append([stream, quality])

        categ = []
        if len(row.findAll('td')) > categ_td_id:
            categ = row.findAll('td')[categ_td_id].text
            categ.strip()
            categ = categ.replace('"','')
            categ = re.split(', |/', categ)

        db_wrapper.add_radio(name.strip(), location.strip(), country.strip(), streams, categ, homepage=url.strip())

        print '-'*80
        print name
        print url
        print location
        print country
        print streams
        print categ



