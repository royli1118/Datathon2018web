#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Created by youshaox on 22/11/18
"""
function:

"""
import sys

#解决 二进制str 转 unicode问题
reload(sys)
sys.setdefaultencoding('utf8')


import urllib2
import urllib
import json
from bs4 import BeautifulSoup




postcode_list = []
postcode = '3008'
list_no = 1
# 每个显示25个，总共80页，显示2000个
list_suffix = 'list-' + str(list_no)
buy_overall_url = 'https://www.realestate.com.au/buy/in-{}/{}?includeSurrounding=false'.format(postcode, list_suffix)

print buy_overall_url
request = urllib2.Request(url=buy_overall_url)
response = urllib2.urlopen(request, timeout=20)
result = response.read()
html = BeautifulSoup(result, 'lxml')
# print html
overall_info_per_house = html.select('article')[1]
print '--------------overall_info_per_house--------------'
print overall_info_per_house
print '--------------overall_info_per_house--------------'

print '--------------detailed_link--------------'
# IndexError: list index out of range

detailed_link = overall_info_per_house.select('a.details-link')
detailed_link = "https://www.realestate.com.au" + detailed_link[0]['href']
# detailed_link = overall_info_per_house.find_all('a', href=True)
print detailed_link
print '--------------detailed_link--------------\n'


print '--------------address--------------'
address = overall_info_per_house.select('h2.residential-card__address-heading')[0].get_text()

print address
print '--------------address --------------'


print '--------------img_link--------------'
img_link = overall_info_per_house.select('img.property-image__img')[0]
img_link = img_link['src']
print img_link
print '--------------img_link --------------'


print '--------------property_type--------------'
property_type = overall_info_per_house.select('span.residential-card__property-type')[0]
property_type = property_type.get_text()
print property_type
print '--------------property_type --------------'


print '--------------property_price--------------'
property_price = overall_info_per_house.select('span.property-price')[0]
property_price = property_price.get_text()
print property_price
print '--------------property_price --------------'


print '--------------property_size--------------'
property_size = overall_info_per_house.select('div.property-size.rui-clearfix')[0]
property_size = property_size.get_text()
print property_size
print '--------------property_size --------------'

request = urllib2.Request(url=detailed_link)
response = urllib2.urlopen(request, timeout=20)
result = response.read()
html = BeautifulSoup(result, 'lxml')

# detailed features
property_features_tags = html.select('div.property-features__feature')
property_features = list()
for feature in property_features_tags:
    feature = feature.get_text()
    property_features.append(feature)
print property_features

"""
{
"address":"505/2 Glenti Place",
"postcode":"3008",
"property_type":"Apartment",
"buy_or_lend":"buy",
"property_price":"$850,000 - $900,000",
"size":"94 m²",
"img_link":"https://i2.au.reastatic.net/800x600/c215d4665ae0d3fc51fe5c3f5e47bbf62010818ca1d6c2b50a40edd4f85cadf3/image.jpg",
"detailed_features":{
    "":"",
}
}
"""
