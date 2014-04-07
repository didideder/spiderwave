#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import HTMLParser
import subprocess
import re
import sys
import urllib
import urllib2

import db_wrapper

RESUME_ID = 108

COUNTRIES = [
"Internet Only",
"GA", # Georgia - the country
"Montserrat",
"Cuba",
"Virgin Islands (US)",
"Virgin Islands (UK)",
"Martinique",
"Cayman Islands",
"Trinidad Tobago",
"Jamaica",
"Barbados",
"Haiti",
"Saint Vincent",
"Afghanistan",
"Albania",
"Algeria",
"American Samoa",
"Andorra",
"Angola",
"Argentina",
"Armenia",
"Australia",
"Austria",
"Azerbaijan",
"Bahrain",
"Bangladesh",
"Belarus",
"Belgium",
"Belize",
"Benin",
"Bermuda",
"Bhutan",
"Bolivia",
"Bosnia and Herzegovina",
"Bosnia",
"Botswana",
"Brazil",
"Brunei Darussalam",
"Bulgaria",
"Burkina Faso",
"Burundi",
"Cambodia",
"Cameroon",
"Canada",
"Canary Islands",
"Cape Verde",
"Caribbean Islands",
"Central African Republic",
"Chad",
"Chile",
"China",
"Christmas Island",
"Cocos Islands",
"Colombia",
"Comoros",
"Congo",
"Cook Islands",
"Costa Rica",
"Cote D'ivoire",
"Saint Lucia",
"Croatia",
"Cyprus",
"Czech Republic",
"Denmark",
"Djibouti",
"DR Congo",
"East Timor",
"Ecuador",
"Egypt",
"El Salvador",
"Equatorial Guinea",
"Eritrea",
"Estonia",
"Ethiopia",
"Falkland Islands",
"Faroe Islands",
"Federated States of Micronesia",
"Fiji",
"Finland",
"France",
"French Guiana",
"French Polynesia",
"Gabon",
"Gambia",
"Georgia",
"Germany",
"Ghana",
"Gibraltar",
"Greece",
"Greenland",
"Guam",
"Guadeloupe",
"Guatemala",
"Guinea",
"Guinea-Bissau",
"Guyana",
"Honduras",
"Hong Kong",
"Hungary",
"Iceland",
"India",
"Indonesia",
"Iran",
"Iraq",
"Ireland",
"Israel",
"Italy",
"Japan",
"Jordan",
"Kazakhstan",
"Kenya",
"Kiribati",
"Kuwait",
"Kyrgyzstan",
"Laos",
"Latvia",
"Lebanon",
"Lesotho",
"Liberia",
"Libya",
"Liechtenstein",
"Lithuania",
"Luxembourg",
"Macau",
"Macedonia",
"Madagascar",
"Malawi",
"Malaysia",
"Maldives",
"Mali",
"Malta",
"Marshall Islands",
"Mauritania",
"Mauritius",
"Mayotte",
"Mexico",
"Moldova",
"Monaco",
"Mongolia",
"Montenegro",
"Morocco",
"Mozambique",
"Myanmar (Burma)",
"Namibia",
"Nauru",
"Nepal",
"Netherlands",
"Netherlands Antilles",
"New Caledonia",
"New Zealand",
"Nicaragua",
"Niger",
"Nigeria",
"Norfolk Island",
"Northern Mariana Islands",
"North Korea",
"Norway",
"Oman",
"Pakistan",
"Palau",
"Palestine",
"Panama",
"Papua New Guinea",
"Paraguay",
"Peru",
"Philippines",
"Poland",
"Portugal",
"Qatar",
"Reunion",
"Romania",
"Russia",
"Rwanda",
"Samoa",
"San Marino",
"Sao Tome-Principe",
"Saudi Arabia",
"Senegal",
"Serbia",
"Seychelles",
"Sierra Leone",
"Singapore",
"Slovakia",
"Slovenia",
"Solomon Islands",
"Somalia",
"South Africa",
"South Korea",
"Spain",
"Sri Lanka",
"St. Helena",
"St. Pierre-Miquelon",
"Sudan",
"Suriname",
"Swaziland",
"Sweden",
"Switzerland",
"Syria",
"Taiwan",
"Tajikistan",
"Tanzania",
"Thailand",
"Togo",
"Tonga",
"Tunisia",
"Turkey",
"Tuvalu",
"Uganda",
"Ukraine",
"United Arab Emirates",
"United Kingdom",
"United States",
"Uruguay",
"Uzbekistan",
"Vanuatu",
"Vatican City",
"Venezuela",
"Vietnam",
"Wallis-Futuna Islands",
"Western Sahara",
"Yemen",
"Zambia",
"Zimbabwe"
]

def get_page(url):
    try:
        soup = BeautifulSoup(get_data(url))
    except:
        return None
    return soup

def get_data(url):
    return urllib2.urlopen(url, timeout=5).read()

def find_nb_page(soup):
    paging_link = soup.findAll('a', {'class':"paging"})
    max = 1
    for link in paging_link:
        nb = int(link.text)
        if nb > max:
            max = nb
    return max

def scrape_da_page(link):

    print "Scraping: %s" % paging_link
    soup = get_page(link)
    if soup is None:
        return
    sections = soup.findAll("tr", {'align':"left", "bgcolor":"#FFFFFF"})
    nb_sections = 0
    for section in sections:
        print "Doing sections %d/%d" % (nb_sections, len(sections))
        nb_sections += 1
        name = section.findAll('td')[1].findAll('a')[0].text
        try:
            name = unicode(name).encode('utf-8')
        except UnicodeDecodeError:
            name = unicode(name.decode('utf-8')).encode('utf-8')

        stream = section.findAll('td')[1].findAll('a')[0]['href']
        stream = "http://vtuner.com/setupapp/guide/asp/"+stream[3:]
        stream = urllib.quote(stream, ":/?=&#" )
        try:
            stream = get_data(stream)
        except:
            print "No stream URL. Moving on."
            continue
        stream_list = [stream]
        if "[Reference]" in stream:
            stream_list = []
            streams = stream.split('\n')
            for s in stream:
                if 'Ref' in s:
                    stream_list.append("http"+s.split('http')[1])

        location = section.findAll('td')[2].text
        country = None

        print "Country: %s" % location
        if "Slovak Republic" in location:
            country = "Slovakia"
            location = location.replace("Slovak Republic", '')
        else:
            for cnt in COUNTRIES:
                if cnt in location:
                    country = cnt
                    location = location.replace(cnt, '')
        if country is None:
            print "No country found. Moving on."
            sys.exit(0)
            continue
        city = location.strip()

        categ = []
        if len(section.findAll('td')) > 3:
            categ = section.findAll('td')[3].text
            categ = re.split(', |/', categ)

        quality = section.findAll('td')[4].text
        quality = html_parser.unescape(quality)
        quality = unicode(quality).encode('utf-8')

        cnt_id = db_wrapper.insert_country(country)

        # Insert a City of a country
        city_id = db_wrapper.insert_city(location, cnt_id)
        # Insert the genre
        genres_id = []
        for cat in categ:
            genres_id.append(db_wrapper.insert_genre(cat))

        stream_id = []
        for st in stream_list:
            try:
                stream_id.append(db_wrapper.insert_streamurl(st))
            except:
                print st
                print stream_list
                print '-'*80
                print name
                print stream
                print country
                print city
                print categ
                print quality

        # Finally, the whole radio
        db_wrapper.insert_radio(name, stream_url_ids=stream_id, genre_ids=genres_id, country_id=cnt_id, city_id=city_id, homepage=url)

        print '-'*80
        print name
        print stream
        print country
        print city
        print categ
        print quality

db_wrapper.connect()

html_parser = HTMLParser.HTMLParser()
soup = get_page("http://vtuner.com/setupapp/guide/asp/BrowseStations/StartPage.asp?sBrowseType=Location")
link_countries = soup.findAll('a')
link_url = []
for link_country in link_countries:
    href = link_country['href']
    if "BrowseStations" not in href or "Category" not in href:
        continue
    url = "http://vtuner.com/setupapp/guide/asp/"+link_country['href'][3:]
    link_url.append(urllib.quote(url, ":/?=&#" ))

resume = 0
for link in link_url:
    resume += 1
    print "%d - %s" % (resume, link)
    if resume < RESUME_ID:
        continue

    try:
        soup = get_page(link)
        if soup is None:
            raise Exception
    except:
        print link
    # We need to find how many pages are there.
    nb_page = find_nb_page(soup)
    for page in range(1, nb_page+1):
        paging_link = link+"&iCurrPage=%d" % page
        scrape_da_page(paging_link)

db_wrapper.disconnect()
