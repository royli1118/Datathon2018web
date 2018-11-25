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
from pybloomfilter import BloomFilter



postcode_list = []
postcode = '3008'
download_bf = BloomFilter(1024 * 1024 * 16, 0.001)


def crawl_by_postcode_buy(postcode):
    """
    Arguments
    =========
    postcode : int
    postcode of the region in the victoira

    Returns
    =======
    arm : int
    the positive integer arm id for this round
    """
    info_houses_list = []
    buy_or_lend = 'buy'
    list_no = 1
    while True:
        try:
            list_suffix = 'list-' + str(list_no)
            buy_overall_url = 'https://www.realestate.com.au/buy/in-{}/{}?includeSurrounding=false'.format(postcode,
                                                                                                           list_suffix)
            overall_request = urllib2.Request(url=buy_overall_url)
            overall_response = urllib2.urlopen(overall_request, timeout=20)
            overall_result = overall_response.read()
            overall_html = BeautifulSoup(overall_result, 'lxml')

            # 挖掘总览中的每一个房子的信息
            for article in overall_html.select('article'):
                info_per_house = {}
                overall_info_per_house = article
                detailed_link = overall_info_per_house.select('a.details-link')
                detailed_link = "https://www.realestate.com.au" + detailed_link[0]['href']
                if detailed_link in download_bf:
                    continue
                else:
                    download_bf.add(detailed_link)

                # print detailed_link
                # 请求细节页
                detailed_request = urllib2.Request(url=detailed_link)
                detailed_response = urllib2.urlopen(detailed_request, timeout=20)
                detailed_result = detailed_response.read()
                detailed_html = BeautifulSoup(detailed_result, 'lxml')
                # print detailed_html
                address = detailed_html.select('h1.property-info-address')[0].get_text()
                property_type = detailed_html.select('span.property-info__property-type')[0].get_text()
                property_price = detailed_html.select('span.property-price.property-info__price')[0].get_text()
                property_size = detailed_html.select('div.property-size.rui-clearfix')[0].get_text()
                img_link = detailed_html.select('div.hero-mosaic__main-photo')[0]
                img_link = img_link.select('img')[0]
                img_link = img_link['src']

                # detailed features
                property_features_tags = detailed_html.select('div.property-features__feature')
                property_features = list()
                for feature in property_features_tags:
                    feature = feature.get_text()
                    property_features.append(feature)

                info_per_house['address'] = address
                info_per_house['postcode'] = postcode
                info_per_house['property_type'] = property_type
                info_per_house['buy_or_lend'] = buy_or_lend
                info_per_house['property_price'] = property_price
                info_per_house['property_size'] = property_size
                info_per_house['img_link'] = img_link
                info_per_house['detailed_features'] = property_features
                info_houses_list.append(info_per_house)
            if list_no>=50:
                print info_houses_list
                break
        # 当该地区所有买的房子都爬完后，退出。
        except IndexError as e:
            print 'index_error'
            print len(info_houses_list)
            print info_houses_list
            print e
            break

        # 每个显示25个，总共80页，显示2000个
        list_no += 25


crawl_by_postcode_buy('3008')


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
