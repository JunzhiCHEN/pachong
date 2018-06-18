# -*- coding: UTF-8 -*-
import os
from config_file import  MYSQL_CONF_PATH, DB_STATUS
os.environ['HILLINSIGHT_MYSQL_CONF'] = MYSQL_CONF_PATH
os.environ['SKY_SERVER_MYSQL_ENV'] = DB_STATUS
from db_conn import _mysql_config


import requests
import json
from cookies import Headers2, GET_COMPANY_URL


url = "https://rong.36kr.com/n/api/dict/area"
req = requests.session()
#requests.utils.add_dict_to_cookiejar(req.cookies, bcookies)

response = req.get(url, headers=Headers2)
city_list = json.loads(response.text)

db = _mysql_config["pachong"]['master']
for one in city_list.get("data", {}).get("data", []):
    result = db.insert("citys", city_id=one.get("id", 0), parent_id=one.get("parentId", 0),
                       feature=one.get("feature", 0), name=one.get("name", ""),
                       disp_order=one.get("dispOrder", 0))
    print result