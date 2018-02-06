#!/usr/bin/python
# coding=utf8
# author: sunyang
# 使用组的方式，来关闭指定的触发器(trigger)

import json
import requests
import sys

# 触发器的名字
trigger_name = "Time synchronization is more than 10 seconds"

# 组的名字
group_name = u"研发测试1网段环境"


##################################################################################

url = "http://192.168.2.193/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}

jsondata = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "admin",
            "password": "smc@z9w5"
        },
        "id": 0
    })





r = requests.get(url,headers=header,data=jsondata)


auth = r.json()['result']

hosts_json ={
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            "name": [group_name],
    },
    "selectHosts": ['hostid'],
    },
    "id": 2,
    "auth": auth
}


hosts = requests.get(url,headers=header,data=json.dumps(hosts_json))

host_list = []
for hostid in hosts.json()['result'][0]['hosts']:
    host_list.append(hostid['hostid'])





t_json = {
    "jsonrpc": "2.0",
    "method": "trigger.get",
    "params": {
        "output": [
            "triggerid",
            "description",
            "priority"
        ],
        "filter": {
            "hostid": host_list,
            "description": trigger_name,
        },
    },
    "auth": auth,
    "id": 1
}


hosts = requests.get(url,headers=header,data=json.dumps(t_json))  


t_list = []
for tid in hosts.json()['result']:
    updata_t = {"jsonrpc": "2.0","method": "trigger.update","params": {"triggerid": tid['triggerid'],"status": 1},"auth": auth,"id": 1}
    updata = requests.get(url,headers=header,data=json.dumps(updata_t))
    print(updata.json())
