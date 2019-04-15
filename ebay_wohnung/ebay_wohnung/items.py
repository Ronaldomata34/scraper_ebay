# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealStateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ad_url = scrapy.Field() #
    place = scrapy.Field() #
    zip_code = scrapy.Field() #
    creation_date = scrapy.Field() #
    room = scrapy.Field() #
    purchase_price = scrapy.Field() #
    number_of_bathrooms = scrapy.Field()  #
    number_of_bedrooms = scrapy.Field() #
    reference = scrapy.Field() #
    floor = scrapy.Field() #
    type_of_apartment = scrapy.Field() #
    whnfl = scrapy.Field() #
    construction_year = scrapy.Field() #
    domestic_equipments = scrapy.Field() #
    heating = scrapy.Field() #
    house_money = scrapy.Field() #
    commission = scrapy.Field() #
    description = scrapy.Field() #
    available_from_month = scrapy.Field() #
    available_from_year = scrapy.Field() #


