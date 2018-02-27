#!/usr/bin/python
# coding=utf8
# author: sunyang
# zabbix认证装饰器


import json
import requests
import settings

ZABBIX_IP = settings.ZABBIX_IP
ZABBIX_USER = settings.ZABBIX_USER
ZABBIX_PASSWD = settings.ZABBIX_PASSWD
url = "http://{ip}/zabbix/api_jsonrpc.php".format(ip=ZABBIX_IP)

def auth():
    try:
        header = {"Content-Type": "application/json"}

        jsondata = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "{user}".format(user=ZABBIX_USER),
                    "password": "{passwd}".format(passwd=ZABBIX_PASSWD)
                },
                "id": 0
            })
        r = requests.get(url,headers=header,data=jsondata)
        auth = r.json()['result']
        return auth
    except:
        print("验证失败,请检查settings配置！")
        exit()
