#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import random
import re
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

from config_file import  MYSQL_CONF_PATH, DB_STATUS
os.environ['HILLINSIGHT_MYSQL_CONF'] = MYSQL_CONF_PATH
os.environ['SKY_SERVER_MYSQL_ENV'] = DB_STATUS
from db_conn import _mysql_config
from cookies import BCOOKIE1


import requests
import json

def get_finance(company_id):
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





    second = random.random()
    time.sleep(second)
    print "-----------------------company_id : %d" % company_id

    url = 'https://rong.36kr.com/n/api/company/%d/finance?asEncryptedTs=0.26437019827021124&asTs=1528670405474' % company_id
    req = requests.session()
    requests.utils.add_dict_to_cookiejar(req.cookies, BCOOKIE1)

    response = req.get(url)
    result = json.loads(response.text)

    if result.has_key("code") and result.get("code")==0:
        finances = result.get('data', [])
        for one in finances:
            finance_amount = one.get('financeAmount', "")
            finance_amount_unit = one.get('financeAmountUnit', '')
            phase = one.get('phase', '')
            participants = one.get('participantVos', [])
            news_url = one.get("newsUrl", "")
            org_name_list = []
            for vos in participants:
                org_name = vos.get('entityName', "")
                org_name_list.append(org_name)
            participant_investor = (', ').join(org_name_list)
            finance_date = one.get('financeDate', 0)
            if finance_date:
                d = datetime.datetime.fromtimestamp(finance_date/1000)
                finance_date_str = d.strftime("%Y-%m-%d %H:%M:%S")
            add_one_to_company_finance(company_id, finance_amount, finance_amount_unit, news_url, participant_investor, phase, finance_date_str)
    else:
        print json.dumps(result)

        pass

def add_one_to_company_finance(company_id, finance_amount, finance_amount_unit, news_url, participant_investor, phase, finance_date):
    db = _mysql_config['pachong']['master']
    result = db.insert('company_fiance', company_id=company_id, finance_amount=finance_amount, finance_amount_unit=finance_amount_unit,
              news_url=news_url, participant_investor=participant_investor, phase=phase, finance_date=finance_date)
    print result
    pass


def get_company_id_list(table_name):
    db = _mysql_config['pachong']['master']
    sql = 'select company_id from %s limit 400, 200 ' % table_name
    result = db.query(sql)
    company_id_list = []
    for one in result:
        company_id_list.append(one['company_id'])
    return company_id_list








if __name__ == '__main__':
    company_id_list = get_company_id_list('new_companys')
    print len(company_id_list)
    num = 1
    for cid in company_id_list:
        print "----------------num: %d" % num
        get_finance(cid)
        num += 1
