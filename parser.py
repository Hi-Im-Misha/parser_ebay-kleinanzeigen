import requests
import json
import re
from bs4 import BeautifulSoup
from time import sleep


filter_value = 80

def get_url():
    for count in range(1, 2):

        url = f"https://www.ebay-kleinanzeigen.de/s-gewerbeimmobilien/seite:{count}/c277"
        r = requests.get(url, allow_redirects=True,headers={
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        soup = BeautifulSoup(r.text, "lxml")
        data = soup.find_all("div", class_="aditem-main")

        for i in data:

            value = i.find("p", class_="aditem-main--middle--price-shipping--price").text
            skip_point = value.replace('.', '')
            skip_VB = skip_point.replace('VB', '1')
            skip_evro = skip_VB.replace('€', '')
            list = skip_evro.split()

            if list[0] == "Z":
                continue
            else:
                list[0] = int(list[0])

            if list[0] >= filter_value or list[0] == 1:
                card_url = "https://www.ebay-kleinanzeigen.de" + i.find("a").get("href")
                yield card_url
            else:
                continue
def array():
    for card_url in get_url():
        print(card_url)
        view_catalog_num = ''.join(re.findall('\d{10}', card_url))

        request_url = "https://www.ebay-kleinanzeigen.de/s-vac-inc-get.json?adId=" + view_catalog_num

        r = requests.get(request_url, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })

        r_catalog = requests.get(card_url, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })

        sleep(1)
        soup = BeautifulSoup(r.text, "lxml")
        soup_catalog = BeautifulSoup(r_catalog.text, "lxml")

        view = r.json()
        view = view.get('numVisits')

        if view > 80:
            data = soup_catalog.find("div", class_="contentbox--vip boxedarticle no-shadow l-container-row")
            name = data.find("h1").text
            value = data.find("h2").text

            yield view, value, card_url, name
        else:
            continue



