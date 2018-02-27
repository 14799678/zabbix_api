#!/usr/bin/python
# coding=utf8
# author: sunyang
# 监控项目(items)的删除和重命名

import json
import requests
import sys
import auth
header = {"Content-Type": "application/json"}


class Get_host_item(object):
    def __init__(self,host,key):
        self.host = host
        self.key = key
        self.auth_id = auth.auth()
        self.list_item = {"jsonrpc": "2.0","method": "host.get","params": {"output": ["hostid"],
                          "filter":{"host":[self.host]}},"auth":self.auth_id,"id": 2}
        hosts = requests.get(auth.url,headers=header,data=json.dumps(self.list_item))
        self.hostid = hosts.json()['result'][0]['hostid']

    def show_item(self):
        item_json = {"jsonrpc": "2.0","method": "item.get","params": {"output": "extend","search":{"key_": self.key},
                         "filter":{"hostid":[self.hostid]},"sortfield": "name"},"auth":self.auth_id,"id": 2}
        result = requests.get(auth.url,headers=header,data=json.dumps(item_json))
        print(result.json()['result'][0]['lastvalue'])

if __name__ == "__main__":
    # 监控的item 如：net.if.in[eth0]

    if len(sys.argv) < 3:
        print(u"请跟参数,参数为 1(主机名字) 2(主机的 监控项名称)")
        exit(1)
    hostname = sys.argv[1]
    item_key = sys.argv[2]
    a = Item_update(hostname,item_key)
    a.show_item()
