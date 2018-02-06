#!/usr/bin/python
# coding=utf8
# author: sunyang
# 针对所有监控的ip进行 监控项的添加


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



trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "tomcat error {HOST.NAME}",
           "expression": "{browser_master1_10.240.67.20:net.tcp.port[,80].min(5m)}=0","priority": 3,},],
           "auth": "66b61273b4d955a6d179a3932ab5329a","id": 4}


hosts = requests.get(url,headers=header,data=json.dumps(hosts_json))


for host in hosts.json()['result']:
    hostid = host['hostid']
    ip = host['interfaces'][0]['ip']
    id = host['interfaces'][0]['interfaceid']
    host_dic[ip] = [hostid,host['host'],id]


print(host_dic)

for i in app_install.sections():
    for app,v in app_install.items(i):

        try:
            # port check
            port = int(v.rstrip())
            print app,port,'port'
            check_port = {"jsonrpc": "2.0","method": "item.create","params": {"name": "%s port check"%app,"key_": "net.tcp.listen[%s]"%v,
                         "hostid": "%s"%host_dic[i][0],"type": 0,"value_type": 3,"interfaceid": "%s"%host_dic[i][2],"delay": 60,'history':7},"auth": auth,"id": 1}
            hosts = requests.get(url,headers=header,data=json.dumps(check_port))

            trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "%s port %s down"%(app,v),
                       "expression": "{%s:net.tcp.listen[%s].max(#3)}=0"%(host_dic[i][1],v),"priority": 3,},],
                       "auth": auth,"id": 4}
            trig = requests.get(url,headers=header,data=json.dumps(trigger))

        except :
            print app,v,'supp'
            # supp
            check_server = {"jsonrpc": "2.0","method": "item.create","params": {"name": "%s process check"%app,"key_": "proc.num[,,all,%s]"%v,
                         "hostid": "%s"%host_dic[i][0],"type": 0,"value_type": 3,"interfaceid": "%s"%host_dic[i][2],"delay": 60,'history':7},"auth": auth,"id": 1}
            hosts = requests.get(url,headers=header,data=json.dumps(check_server))

            trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "%s process down"%app,
                       "expression": "{%s:proc.num[,,all,%s].max(#3)}=0"%(host_dic[i][1],v),"priority": 3,},],
                       "auth": auth,"id": 4}
            trig = requests.get(url,headers=header,data=json.dumps(trigger))
        print(hosts.json())
        print(trig.json())
