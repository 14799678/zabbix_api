#!/usr/bin/python
# coding=utf8
# author: sunyang
# 检查简本，用来检查 conf/port.conf 配置文件里面的ip是否被zabbix监控


import json
import requests
import ConfigParser


host_dic = {}


class myconf(ConfigParser.ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


app_install = myconf()

app_install.read('conf/port.conf')


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
        ],
    },
    "id": 2,
    "auth": auth
}




trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "tomcat error {HOST.NAME}",
           "expression": "{browser_master1_10.240.67.20:net.tcp.port[,80].min(5m)}=0","priority": 3,},],
           "auth": "66b61273b4d955a6d179a3932ab5329a","id": 4}


hosts = requests.get(url,headers=header,data=json.dumps(hosts_json))

for host in hosts.json()['result']:
    hostid = host['hostid']
    ip = host['interfaces'][0]['ip']
    id = host['interfaces'][0]['interfaceid']
    host_dic[ip] = [hostid,host['host'],id]



for i in app_install.sections():
    for app,v in app_install.items(i):
        if i in host_dic:
            print(i,'ok')
        else:
            print(i,'no host_dic')
