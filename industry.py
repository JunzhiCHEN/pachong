# -*- coding: UTF-8 -*-
import os
from config_file import  MYSQL_CONF_PATH, DB_STATUS
os.environ['HILLINSIGHT_MYSQL_CONF'] = MYSQL_CONF_PATH
os.environ['SKY_SERVER_MYSQL_ENV'] = DB_STATUS
from db_conn import _mysql_config


import requests
import json
import time
import random
from cookies import Headers2, GET_COMPANY_URL
from sort_of_company import Fisrt_Level

db = _mysql_config['pachong']['master']


for k in Fisrt_Level:
    url = "https://rong.36kr.com/n/api/column/0/company?industry=%s&sortField=HOT_SCORE&p=1" % k
    req = requests.session()
    # requests.utils.add_dict_to_cookiejar(req.cookies, bcookies)

    response = req.get(url, headers=Headers2)
    result = json.loads(response.text)
    label_list = result.get("data", {}).get("label", [])
    for one in label_list:
        result = db.insert('industry', label_id=one.get("id", 0), name=one.get("name", ""),
                               industry=k, industry_name=Fisrt_Level.get(k, ""))
        print result
    print k
    seconds = random.random()
    time.sleep(round(seconds*20, 2))



