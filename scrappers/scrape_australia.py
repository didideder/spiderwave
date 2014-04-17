#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

import db_wrapper
import scrape_mike as ssm

db_wrapper.connect()

url = "http://www.australianliveradio.com/"
soup = ssm.get_page(url)
radios = soup.findAll("div", {"class" : "thetable3"})
for section in radios:
    data = section.find("table").find("tbody")
    ssm.scrape(
            data,
            name_td_id=0, location_td_id=1, stream_td_id=3, categ_td_id=4,
            country="Australia")

db_wrapper.disconnect()
