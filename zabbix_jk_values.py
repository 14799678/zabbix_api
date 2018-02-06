#!/usr/bin/python
# coding=utf8
# author: sunyang
# 监控项目(items)的删除和重命名

import json
import requests
import sys





url = "http://192.168.2.183/zabbix/api_jsonrpc.php"
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
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": auth
}



class Item_update(object):
    def __init__(self,key,rename=None):
        self.hostid_value = {}
        self.host_id_list = []
        self.name_value = {}
        self.key = key
        self.rename = rename
        self.list_item = {"jsonrpc": "2.0","method": "item.get","params": {"output": "extend","search":{"key_": self.key},"sortfield": "name"},"auth":auth,"id": 2}
        hosts = requests.get(url,headers=header,data=json.dumps(self.list_item))
        for i in hosts.json()['result']:
            print(i)
            self.hostid_value[i["hostid"]] = i["lastvalue"] 
            print("------------")
        print(self.hostid_value)
        self.host_id_list = self.hostid_value.keys()

    def get_group_name(self):
        hosts_json ={"jsonrpc": "2.0","method": "hostgroup.get","params": {"output": "extend","hostids": self.host_id_list,"selectHosts":["hostid"]},
                     "id": 2,"auth": auth}
        groups = requests.get(url,headers=header,data=json.dumps(hosts_json))
        for num,i in enumerate(groups.json()["result"]):
            print(num,i)
            for host_id in i['hosts']:
                if host_id['hostid'] in self.hostid_value:
                    self.name_value[i['name']] = self.hostid_value[host_id['hostid']]
                    break

        print(self.name_value)

a = Item_update('car_num')
a.get_group_name()
