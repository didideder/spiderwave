#! /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import errno
import HTMLParser
import re
import socket
import sys
import urllib
import urllib2

import db_wrapper

RESUME_ID = 0
PAGE_ID = 0

US_STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

COUNTRIES = [
"Internet Only",
"Anguilla",
"Saint Kitts-Nevis",
"Antigua",
"Aruba",
"Dominica",
"Grenada",
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
"Puerto Rico",
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
"Bahamas",
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
"Ivory Coast",
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

def get_data(url, limit=False):
    try:
        temp = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if e.code == 302:
            return e.geturl()
        else:
            raise e

    if limit:
        data = temp.read(8192)
        # We have the real stream, so it's only data here.
        # Return the URL
        if len(data) == 8192:
            return url
        # If there is multiple line in the data we just got, we should return
        # the URL, we probably got a metadata file containing the stream URL.
        if data.count('\n') > 2:
            # If it's an ASF containing only multiple stream for the same
            # radio, it will be handled.
            if "[Reference]" in data:
                return data
            # Other than that, we don't take care of it here.
            return temp.geturl()
        elif '<asx version="3.0"' in data.lower():
            return url
        return data
    return temp.read()

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
            stream = get_data(stream, limit=True)
        except urllib2.URLError as e:
            print e
            continue
        except urllib2.HTTPError as e:
            print e
            if e.code in [404, 400]:
                continue
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                print "Connection reset by peer."
                continue
        except:
            print "No stream URL. Moving on."
            print name
            print stream
            sys.exit(0)
        stream_list = [stream]
        if "[Reference]" in stream:
            stream_list = []
            streams = stream.split('\n')
            for s in streams[1:]:
                if 'Ref' in s:
                    stream_list.append("http"+s.split('http')[1].strip())

        location = section.findAll('td')[2].text
        country = None

        print "Country: %s" % location
        if "State" in paging_link:
            for st, state in US_STATES.iteritems():
                if st in location:
                    country = "United States - %s" % state
                    location = location.replace(st, '')
                elif state in location:
                    country = "United States - %s" % state
                    location = location.replace(state, '')
            if country is None and "Internet Only" in location:
                state = paging_link.split('State=')[1].split('&i')[0]
                country = "United States - %s" % state
        elif "Slovak Republic" in location:
            country = "Slovakia"
            location = location.replace("Slovak Republic", '')
        elif "Micronesia"in location:
            country = "Federated States of Micronesia"
            location = location.replace("Micronesia", '')
        elif "Brunei" in location:
            country = "Brunei Darussalam"
            location = location.replace("Brunei", '')
        else:
            for cnt in COUNTRIES:
                if cnt in location:
                    country = cnt
                    location = location.replace(cnt, '')

        # Some radios are misplaced in United States
        if country is None and "State" in paging_link:
            for cnt in COUNTRIES:
                if cnt in location:
                    country = cnt
                    location = location.replace(cnt, '')

        if country is None:
            # This happen only one time but, still.
            if "GA" in location:
                country = "Georgia"
                location = location.replace("Georgia", '')
            if country is None:
                print "No country found. Moving on."
                sys.exit(0)
        city = location.strip()
        country = country.strip()
        if city == "":
            city = country

        categ = []
        if len(section.findAll('td')) > 3:
            categ = section.findAll('td')[3].text
            categ = re.split(', |/', categ)

        # We only have on information about quality, so assume it's the same for all..
        quality = section.findAll('td')[4].text
        quality = html_parser.unescape(quality)
        quality = quality.replace("MP3", '')
        quality = unicode(quality).encode('utf-8')
        try:
            quality = int(non_decimal.sub('', quality))
        except ValueError:
            quality = 0

        streams = []
        for st in stream_list:
            streams.append([st, quality])

        # Finally, the whole radio
        db_wrapper.add_radio(name.strip(), city, country, streams, categ, homepage=url.strip())

        print '-'*80
        print name
        print stream_list
        print country
        print city
        print categ
        print quality


db_wrapper.connect()
non_decimal = re.compile(r'[^\d.]+')

html_parser = HTMLParser.HTMLParser()
soup = get_page("http://vtuner.com/setupapp/guide/asp/BrowseStations/StartPage.asp?sBrowseType=Location")
if soup is None:
    print "Could not start."
    sys.exit(0)
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

    do_scrape = True
    nb_page = 1
    max_page = 2
    if PAGE_ID != 0:
        nb_page = PAGE_ID
        # So we don't fell here again
        PAGE_ID = 0
        # This is seriously broken and ugly.
        # We assume there will be a next page, but maybe there won't be.
        max_page = nb_page + 1

    while do_scrape:
        paging_link = link+"&iCurrPage=%d" % nb_page
        if nb_page > max_page:
            do_scrape = False
            continue
        scrape_da_page(paging_link)
        max_page = find_nb_page(get_page(paging_link))
        nb_page += 1

db_wrapper.disconnect()
