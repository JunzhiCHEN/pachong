#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import random
import re
reload(sys)
sys.setdefaultencoding('utf-8')

from config_file import  MYSQL_CONF_PATH, DB_STATUS
os.environ['HILLINSIGHT_MYSQL_CONF'] = MYSQL_CONF_PATH
os.environ['SKY_SERVER_MYSQL_ENV'] = DB_STATUS
from db_conn import _mysql_config


import requests
import json

total_page_num = 0
on_page = 1


def get_base_info_of_company(page=1):

    bcookies = {
        "Hm_lpvt_713123c60a0e86982326bae1a51083e1":"1528448977",
        "Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3":"1528448937",
        "Hm_lvt_713123c60a0e86982326bae1a51083e1":"1527238009,1528448960",
        "Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3":"1528448830,1528448878",
        "MEIQIA_EXTRA_TRACK_ID":"0v3gejYvOSnYvLSUkFnVqyeMCS8",
        "Z-XSRF-TOKEN":"eyJpdiI6IkVEb0gwbWYxQUY5ZjByenBnNTlJRHc9PSIsInZhbHVlIjoiWnVaa2dZTlZXK1ROaFpKc0Y1aXJzWW90XC8wZWhnMU9PVzQ2XC9ScENmMjc5NTlicW1GQ055eFlNV2p1d0h5ckQ2czcwQmpjK09VQUdyMFVxZFlHUDlJQT09IiwibWFjIjoiYzE5MmU0NjY5OWQxNWQxYWI4NjY2NGJjMGRiZmU0OTUwM2ZhYmU0N2FjNWE1YWE4NDI0OWFkYzExN2EyYWJhYyJ9",
        "_ga":"GA1.2.2053638286.1528448830",
        "_kr_p_se":"a7515d9e-be54-4b4d-a693-e842a388aa56",
        "acw_tc":"AQAAAG7kaFvhOAwAHn7ycs+2YM+CjIgJ",
        "device-uid":"e05356f0-de44-11e7-93ae-0519172dd41b",
        "download_animation":"1",
        "kr_plus_id":"200046671",
        "kr_plus_token":"8lJSnnpSv7AnKdhMzV3ONPIIDBly537_5362____",
        "kr_plus_utype":"0",
        "kr_stat_uuid":"jJeSr25216288",
        "krchoasss":"eyJpdiI6ImcyUnlaQ0NvXC9aNkc4MDdxaTZ1aG9BPT0iLCJ2YWx1ZSI6IlFQMmtMVXVcL25oMFhWbDFBSjBlUEhqOE9XTnB2R3FmSndCQ3RDNzRXTU1ySklxNkhLa29HXC8yanJaWlRqdmhqcmVsaDg1Q3Y5RXNHT1JvXC9XRms3UVhRPT0iLCJtYWMiOiI3ZTY4N2IwYWExODhjMmViOGQyNjE1ZWM1YjU1YTBkZjM3ZGUwMTg0NjJiMzU1ZjM3NTlkZmNiMDc5ZGQ5NThmIn0%3D",
        "krid_user_id":"200046671",
        "krid_user_version":"2",
        "ktm_source":"pcheader",
        "kwlo_iv":"1h",
        "sensorsdata2015jssdkcross":"%7B%22distinct_id%22%3A%22163967a94b61a1-04a604d8caba05-33637606-1024000-163967a94b7995%22%2C%22%24device_id%22%3A%22163967a94b61a1-04a604d8caba05-33637606-1024000-163967a94b7995%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D"
    }

    total_page_num = 168
    while (page < total_page_num):
        second = random.randint(1, 5)
        time.sleep(second)
        print "-----------------------page : %d" % page
        #url = 'https://rong.36kr.com/n/api/search/company?asEncryptedTs=-0.9324324455397508&asTs=1528635494638&kw=人工智能&sortField=MATCH_RATE&p=%s' % page
        url = 'https://rong.36kr.com/n/api/column/0/company?industry=AI&p=%s' % page
        req = requests.session()
        requests.utils.add_dict_to_cookiejar(req.cookies, bcookies)

        response = req.get(url)
        result = json.loads(response.text)
        print "result"

        if result.has_key("code") and result.get("code")==0:
            total_page_num = result.get("data", {}).get("pageData", {}).get("totalPages", 0)

            data_list = result.get("data", {}).get("pageData", {}).get("data", [])
            for one in data_list:
                id = one.get("id", 0)
                name = one.get("name", "")
                brief = one.get("brief", "")
                phase = one.get("phase", "")
                industry = one.get('industry', "")
                industry_str = one.get('industryStr', "")
                logo = one.get('logo', "")
                city = one.get('city', 0)
                city_str = one.get('cityStr', "")
                tags_list = one.get('tags', [])
                tags = (',').join(tags_list)
                label_list = one.get("labelSource", [])
                label_source = (',').join(label_list)
                invest_parts = (',').join(one.get('investParts', []))

                add_one_all_company(id, name, brief, phase, industry, industry_str, logo, city, city_str, tags, label_source, invest_parts)
        page += 1
    return 0


def add_one_all_company(id, name, brief, phase, industry, industry_str, logo, city, city_str, tags, label_sources, invest_parts):
    db = _mysql_config['pachong']['master']
    result = db.insert('all_companys', company_id=id, name=name, brief=brief, phase=phase,
                       industry=industry, industry_str=industry_str, logo=logo,
                       city=city, city_str=city_str, tags=tags, label_sources=label_sources,
                       invest_parts=invest_parts)
    print result

if __name__ == '__main__':
    on_page = 1
    get_base_info_of_company(on_page)




