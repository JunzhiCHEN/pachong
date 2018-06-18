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
from cookies import Headers2
from sort_of_company import PHASE_SORT



def get_label_info(offset, size):
    db = _mysql_config['pachong']['master']
    sql = "select * from industry order by id limit %d, %d " % (offset, size)
    result = db.query(sql)
    return list(result)



def grab_all_data_by_label(page, page_num):
    if page <1 :
        return False
    result = get_label_info((page-1)*page_num, page_num)
    for one in result:
        industry = one.get("industry", "")
        label_id = one.get("label_id", "")
        get_base_info_of_company(industry, label_id)

def get_base_info_of_company(industry, label_id):
    phase_list = [ "SEED", "ANGEL", "PRE_A", "A", "A_PLUS", "PRE_B", "B", "B_PLUS", "C", "C_PLUS", "D", "E" ]
    #phase_list = [ "SEED"]
    for one_phase in phase_list:
        total_page_num = 1000
        page = 1
        while (page <= total_page_num):
            second = random.randint(1, 20)
            second1 = round(random.random(), 2)
            time.sleep(second + second1)
            print "=======================phase: %s" % one_phase
            print "-----------------------page : %d" % page
            print "-----------------------total_page: %d" % total_page_num
            url = "https://rong.36kr.com/n/api/column/0/company?phase=%s&industry=%s&label=%d&sortField=HOT_SCORE&p=%d" % (one_phase, industry, label_id, page)
            req = requests.session()
            #requests.utils.add_dict_to_cookiejar(req.cookies, bcookies)

            response = req.get(url, headers=Headers2)
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

                    add_one_all_company(id, name, brief, phase, industry, industry_str, logo, city, city_str, tags, label_source, invest_parts, label_id)
            else:
                print json.dumps(result)
                break
            page += 1
    return 0


def add_one_all_company(id, name, brief, phase, industry, industry_str, logo, city, city_str, tags, label_sources, invest_parts, label_id):
    db = _mysql_config['pachong']['master']
    result = db.insert('all_companys', company_id=id, name=name, brief=brief, phase=phase,
                       industry=industry, industry_str=industry_str, logo=logo,
                       city=city, city_str=city_str, tags=tags, label_sources=label_sources,
                       invest_parts=invest_parts, label_id=label_id)
    print result

if __name__ == '__main__':
    on_page = 1
    #get_base_info_of_company(on_page)
    grab_all_data_by_label(1, 1)




