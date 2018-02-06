#!/usr/bin/python
# coding=utf8
# author: sunyang
# 监控项目(items)的删除和重命名

import json
import requests
import sys





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
    def __init__(self,name,rename=None):
        self.itemid_list = []
        self.name = name
        self.rename = rename
        self.list_item = {"jsonrpc": "2.0","method": "item.get","params": {"output": "extend","filter":{"name": self.name},"sortfield": "name"},"auth":auth,"id": 2}
        hosts = requests.get(url,headers=header,data=json.dumps(self.list_item))
        for i in hosts.json()['result']:
            self.itemid_list.append(i['itemid'])

    def item_rename(self):
        for id in self.itemid_list:
            update_item = {"jsonrpc": "2.0","method": "item.update","params": {"itemid": id,"name": self.rename},"auth":auth,"id": 2}
            
            result = requests.get(url,headers=header,data=json.dumps(update_item))
            print(result.json())


    def del_item(self):
        d_item = {"jsonrpc": "2.0","method": "item.delete","params": self.itemid_list,"auth": auth,"id": 1}
        result = requests.get(url,headers=header,data=json.dumps(d_item))
        print(result.json())




if __name__ in '__main__': 
    if len(sys.argv) == 4:
        fun,name,rename = sys.argv[1:]
    elif len(sys.argv) == 3:
        fun,name = sys.argv[1:]
        rename = None
    else:
        print("function name *********","del_item","item_rename","**********")
        print("python scpirt name <function name> <item name> <update item name>")
        exit()
    item_object = Item_update(name,rename)
    func = getattr(item_object, fun) 
    func()
