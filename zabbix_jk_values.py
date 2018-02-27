#!/usr/bin/python
# coding=utf8
# author: sunyang
# 监控项目(items)的删除和重命名

import json
import requests
import sys
import auth
header = {"Content-Type": "application/json"}


class Item_update(object):
    def __init__(self,key,rename=None):
        self.hostid_value = {}
        self.name_value = {}
        self.key = key
        self.rename = rename
        auth_id = auth.auth()
        self.list_item = {"jsonrpc": "2.0","method": "item.get","params": {"output": "extend","search":{"key_": self.key},
                         "selectInterfaces": ["interfaceid","ip"],"sortfield": "name"},"auth":auth_id,"id": 2}
        hosts = requests.get(auth.url,headers=header,data=json.dumps(self.list_item))
        for i in hosts.json()['result']:
            self.hostid_value[i["interfaces"][0]["ip"]] = i["lastvalue"] 

    def show_sort(self):
        sort_list = sorted(self.hostid_value.items(),key = lambda x:int(x[1]),reverse = True)
        for line in sort_list:
            print(line)

    def show_dic(self):
        print(self.hostid_value)

if __name__ == "__main__":
    # 监控的item 如：net.if.in[eth0]

    if len(sys.argv) == 1:
        print(u"请跟参数,参数为 item的 key信息来获取所有主机的最后一次数据")
        exit(1)

    item_key = sys.argv[1]
    status_name = sys.argv[2]
    a = Item_update(item_key)
    getattr(a,status_name)()
