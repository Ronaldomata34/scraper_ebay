import re

import scrapy
from bs4 import BeautifulSoup
from dateutil import parser


from ebay_wohnung.items import RealStateItem

class EbayScraper(scrapy.Spider):
    base_url = 'https://www.ebay-kleinanzeigen.de'
    name = 'EbayScraper'
    allowed_domains = ['ebay-kleinanzeigen.de']
    start_urls = ['https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/anzeige:angebote/c196']

    def get_zip_code(self, str):
        print(str)
        zip_code = re.findall(r'\d+', str)
        print(zip_code)
        return zip_code[0]

    def clean_details(self, lista):
        data = []
        for el in lista:
            el = el.replace('\n','').replace(' ','')
            if el:
                data.append(el)
        if len(data) == 3:
            return data
        return False


    def parse(self, response):
        if response.status == 200:
            ads = response.css('article.aditem')
            for ad in ads:
                item = RealStateItem()
                ad_main = ad.css('div.aditem-main')
                ad_detail = ad.css('div.aditem-details')
                details = ad_detail.css('::text').extract()
                clean_details = self.clean_details(details)
                more_info = ad_main.css('p')[1].css('::text').extract()
                item['zip_code'] = clean_details[1]
                item['place'] = clean_details[2]
                item['ad_url'] =  self.base_url + ad_main.css('h2 a.ellipsis ::attr(href)').extract_first()
                yield scrapy.Request(item['ad_url'], callback=self.parse_ad, meta={'item': item})

            if response.css('a.pagination-next'):
                yield scrapy.Request(self.base_url + response.css('a.pagination-next ::attr(href)').extract_first(), callback=self.parse)

    def parse_ad(self, response):
        if response.status == 200:
            item = response.meta['item']

            soup = BeautifulSoup(response.body, 'html.parser')
            item['description'] = soup.find('p', {'id': 'viewad-description-text'}).text or None
            raw_price = soup.find('h2', {'id':'viewad-price'}).text.replace('.','')
            price = re.findall(r'\d+', raw_price)
            if price:
                item['purchase_price'] = float(price[0])
            else:
                item['purchase_price'] = None
            #raw_price = response.css('h2#viewad-price ::text').extract_first().replace('.','')
            #price = re.findall(r'\d+', raw_price)
            keys = []
            raw_keys = soup.find_all('dt', {'class': 'attributelist--key'})
            for k in raw_keys:
                keys.append(k.text)
            values = []
            raw_values = soup.find_all('dd', {'class': 'attributelist--value'})
            for v in raw_values:
                values.append(v.text.replace('\n','').replace('  ',''))
            print(keys)
            print(values)

            for i, k in enumerate(keys):
                if k == 'Erstellungsdatum:':
                    item['creation_date'] = parser.parse(values[i]).isoformat()
                elif k == 'Zimmer:':
                    item['room'] = float(values[i].replace(',','.'))
                elif k == 'Anzahl Schlafzimmer:':
                    item['number_of_bedrooms'] = float(values[i].replace(',','.'))
                elif k == 'Anzahl Badezimmer:':
                    item['number_of_bathrooms'] = float(values[i].replace(',','.'))
                elif k == 'Etage:':
                    item['floor'] = float(values[i].replace(',','.'))
                elif k == 'Anzeigennummer:':
                    item['reference'] = values[i]
                elif k == 'Wohnungstyp:':
                    item['type_of_apartment'] = values[i]
                elif k == 'Wohnfläche (m²):':
                    item['whnfl'] = float(values[i].replace(',','.'))
                elif k == 'Baujahr:':
                    item['construction_year'] = int(values[i])
                elif k == 'Heizungsart:':
                    item['heating'] = values[i]
                elif k == 'Ausstattung:':
                    item['domestic_equipments'] = values[i].split(',')
                elif k == 'Hausgeld (€):':
                    item['house_money'] = float(values[i].replace(',','.'))
                elif k == 'Provision:':
                    if values[i].startswith('Mit'):
                        item['commission'] = True
                    else:
                        item['commission'] = False
                elif k == 'Verfügbar ab Monat:':
                    item['available_from_month'] = int(values[i])
                elif k == 'Verfügbar ab Jahr:':
                    item['available_from_year'] = int(values[i])
            yield item



