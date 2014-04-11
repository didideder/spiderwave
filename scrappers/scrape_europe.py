#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import subprocess
import re
import sys
import urllib2

import db_wrapper

COUNTRIES = [
"Internet Only",
"Kosovo",
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

def get_page( url ):
    opener = urllib2.build_opener()
    data = opener.open(url).read()
    soup = BeautifulSoup(data)
    return soup

db_wrapper.connect()
non_decimal = re.compile(r'[^\d.]+')
soup = get_page("http://www.listenlive.eu/index.html")
countries = soup.find("table", {"id" : "thetable"})

for row in countries.findAll('tr'):
    link = row.findAll('td')[0].findAll('a')[0]
    country_name = link.text
    found = False
    if "Vatican State" in country_name:
        country_name = "Vatican City"
    for cnt in COUNTRIES:
        if cnt in country_name:
            found = True
    if found == False:
        print "Country (%s) not found in list. Moving on." % country_name
        sys.exit(0)

    cnt_id = db_wrapper.insert_country(country_name.strip())
    country = "http://www.listenlive.eu/"+link['href']

    soup = get_page(country)
    radios = soup.find("table", {"id" : "thetable3"})
    for row in radios.findAll('tr'):
        name_link = row.findAll('td')[0].findAll('a')

        location = row.findAll('td')[1].text
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

        stream_href_list = row.findAll('td')[3].findAll('a')
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
        if len(row.findAll('td')) > 4:
            categ = row.findAll('td')[4].text
            categ.strip()
            categ = categ.replace('"','')
            categ = re.split(', |/', categ)

        print '-'*80
        print name
        print url
        print location
        print country_name
        print streams
        print categ

        # Insert a City of a country
        city_id = db_wrapper.insert_city(location.strip(), cnt_id)
        # Insert the genre
        genres_id = []
        for cat in categ:
            genres_id.append(db_wrapper.insert_genre(cat.strip()))

        st_ids = []
        for st in streams:
            st_ids.append(db_wrapper.insert_streamurl(st[0].strip(), st[1]))

        # Finally, the whole radio
        db_wrapper.insert_radio(name.strip(), stream_url_ids=st_ids, genre_ids=genres_id, country_id=cnt_id, city_id=city_id, homepage=url.strip())


# db_wrapper.disconnect()
