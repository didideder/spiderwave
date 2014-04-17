#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import db_wrapper
import scrape_mike as ssm

url = "http://www.canadianwebradio.com/"
soup = ssm.get_page(url)
countries = soup.find("table", {"id" : "thetable"})

db_wrapper.connect()

# Get every countries's page
for row in countries.findAll('tr'):
    link = row.findAll('td')[0].findAll('a')[0]
    soup = ssm.get_page(url + link['href'])
    data = soup.find("table", {"id" : "thetable3"})
    ssm.scrape(
        data,
        name_td_id=0, location_td_id=2, stream_td_id=4, categ_td_id=5,
        country="Canada")

db_wrapper.disconnect()
