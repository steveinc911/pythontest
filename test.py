from bs4 import BeautifulSoup
import requests
import re
import time

propertiesWithTours = []


root = 'http://www.rightmove.co.uk'
url = root + '/property-for-sale/find.html?locationIdentifier=OUTCODE^1863&insId=1&numberOfPropertiesPerPage=48&areaSizeUnit=sqft&googleAnalyticsChannel=buying'

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'}

result = requests.get(url, headers=headers)

c = result.content

soup = BeautifulSoup(c)

summary = soup.find_all('a',{'class': 'propertyCard-link'})



for x in summary:
    detailURL = root + x.get('href')
    detailResult = requests.get(detailURL, headers=headers)
    dc = detailResult.content
    detailSoup = BeautifulSoup(dc)
    tourLinks = detailSoup.find_all('a',  {"id" : re.compile('virtualTour.*')})
    if len(tourLinks) > 0 :
        links = []
        for l in tourLinks:
            links.append(root + l.get('href'))
        item = {'detailURL': detailURL, 'tourLinks': links}
        print(item)
        propertiesWithTours.append(item)
