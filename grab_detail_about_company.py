#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import random
import datetime
import re
reload(sys)
sys.setdefaultencoding('utf-8')

from config_file import  MYSQL_CONF_PATH, DB_STATUS
os.environ['HILLINSIGHT_MYSQL_CONF'] = MYSQL_CONF_PATH
os.environ['SKY_SERVER_MYSQL_ENV'] = DB_STATUS
from db_conn import _mysql_config
from cookies import Headers2


import requests
import json

def get_intro(table_name, page, page_num):
    company_id_list = get_company_id_list(table_name, page, page_num)

    for company_id in company_id_list:
        second = random.randint(1, 20)
        second1 = round(random.random(), 2)
        time.sleep(second + second1)
        print "-----------------------company_id : %d" % company_id

        url = "https://rong.36kr.com/n/api/company/%d?asEncryptedTs=-0.9964018349496853&asTs=1529327641274" % company_id
        req = requests.session()
        #requests.utils.add_dict_to_cookiejar(req.cookies, BCOOKIE1)

        response = req.get(url, headers=Headers2)
        result = json.loads(response.text)

        if result.has_key("code") and result.get("code")==0:
            one_company = result.get('data', {})
            if one_company:
                full_name = one_company.get('fullName', "")
                intro = one_company.get('intro', "")
                address1 = one_company.get('address1Desc',  "")
                address2 = one_company.get('address2Desc',  "")
                remark_name = one_company.get('remarkName', "")
                project_stat = one_company.get('projectStatHeader', {})
                phase = project_stat.get('phase', "")
                funds_amount = project_stat.get("fundsAmount", "")
                funding = project_stat.get("funding", "")
                name = one_company.get("name", "")
                add_one_to_company_detail(company_id, full_name, phase, funds_amount, funding, intro, address1, address2,
                                          remark_name, name)
            else:
                print json.dumps(result)
                break
        else:
            print json.dumps(result)
            break

        url = 'https://rong.36kr.com/n/api/company/%d/finance?asEncryptedTs=-0.9964018349496853&asTs=1529327641274' % company_id
        req = requests.session()
        #requests.utils.add_dict_to_cookiejar(req.cookies, BCOOKIE1)

        response = req.get(url, headers=Headers2)
        result = json.loads(response.text)

        if result.has_key("code") and result.get("code") == 0:
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
                    d = datetime.datetime.fromtimestamp(finance_date / 1000)
                    finance_date_str = d.strftime("%Y-%m-%d %H:%M:%S")
                add_one_to_company_finance(company_id, finance_amount, finance_amount_unit, news_url,
                                           participant_investor, phase, finance_date_str)

        url = "https://rong.36kr.com/n/api/company/%d/news?asEncryptedTs=0.5165420012855644&asTs=1529332370259" % company_id
        req = requests.session()
        # requests.utils.add_dict_to_cookiejar(req.cookies, BCOOKIE1)

        response = req.get(url, headers=Headers2)
        result = json.loads(response.text)
        if result.has_key("code") and result.get("code") == 0:
            news_list = result.get("data", [])
            for one in news_list:
                add_one_to_news(one.get("title", ""), one.get("newsType", ""), one.get("source", ""),
                                one.get("publishDateStr", ""), one.get("newsUrl", ""), company_id)




def add_one_to_company_detail(company_id, full_name, phase, funds_amount, funding, intro, address1, address2, remark_name, name):
    db = _mysql_config['pachong']['master']
    result = db.insert('company_detail', company_id=company_id, full_name=full_name,
                       phase=phase, funds_amount=funds_amount, funding=funding, intro=intro,
                       address1=address1, address2=address2, remark_name=remark_name, name=name)

def add_one_to_company_finance(company_id, finance_amount, finance_amount_unit, news_url, participant_investor, phase, finance_date):
    db = _mysql_config['pachong']['master']
    result = db.insert('company_fiance', company_id=company_id, finance_amount=finance_amount, finance_amount_unit=finance_amount_unit,
              news_url=news_url, participant_investor=participant_investor, phase=phase, finance_date=finance_date)

def add_one_to_news(title, news_type, source, publish_date, news_url, company_id):
    db = _mysql_config['pachong']['master']
    result = db.insert("news", title=title, news_url=news_url, news_type=news_type,
                       source=source, publish_date=publish_date, company_id=company_id)


def get_company_id_list(table_name, page, page_num):
    db = _mysql_config['pachong']['master']
    if page < 1:
        return False
    sql = 'select company_id from %s limit %d, %d  ' % (table_name, (page-1)*page_num, page_num)
    result = db.query(sql)
    company_id_list = []
    for one in result:
        company_id_list.append(one['company_id'])
    return company_id_list








if __name__ == '__main__':
    page = 1
    page_num = 2
    print "---------------------page: %d" % page
    print "---------------------page_num: %d" % page_num
    get_intro("all_companys", page, page_num)
