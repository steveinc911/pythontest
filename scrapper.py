from bs4 import BeautifulSoup
import requests
import json
import re


propertiesWithTours = []


root = 'http://www.rightmove.co.uk'

def scrape(indx):
    url = root + '/api/_search?locationIdentifier=OUTCODE%5E1863&numberOfPropertiesPerPage=48&radius=0.0&sortType=2&index='+str(indx)+'&viewType=LIST&channel=BUY&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false&viewport='

    headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'}

    listResult = requests.get(url, headers=headers)

    listData = json.loads(listResult.text)

    for p in listData['properties']:
        if p['numberOfVirtualTours'] > 0:
            detailURL = root + p['propertyUrl']
            detailResult = requests.get(detailURL, headers=headers)
            dc = detailResult.content
            detailSoup = BeautifulSoup(dc)
            tourLinks = detailSoup.find_all('a',  {"id" : re.compile('virtualTour.*')})
            links = []
            for l in tourLinks:
                links.append(root + l.get('href'))
            p['tourLinks'] = links
            propertiesWithTours.append(p)


    if int(listData['pagination']['page']) < int(listData['pagination']['total']):
        scrape(listData['pagination']['next'])
scrape(0)

for prop in propertiesWithTours:
    print(prop)
