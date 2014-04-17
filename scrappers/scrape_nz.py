#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

import db_wrapper
import scrape_mike as ssm

db_wrapper.connect()

url = "http://www.nzradioguide.co.nz/"
soup = ssm.get_page(url)
data = soup.find("table", {"id" : "thetable3"})
ssm.scrape(
        data,
        name_td_id=0, location_td_id=1, stream_td_id=3, categ_td_id=4,
        country="New Zealand")

db_wrapper.disconnect()
