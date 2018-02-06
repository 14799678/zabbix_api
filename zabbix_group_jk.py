#!/usr/bin/python
# coding=utf8
# author: sunyang
# 使用组的方式来对服务器添加监控

import json
import requests
import sys
import ConfigParser



# 组的名字
group_name = u"吉利汽车"


##################################################################################




class myconf(ConfigParser.ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


app_install = myconf()

app_install.read('conf/port.conf')

host_dic = {}
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



h_json ={
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "filter":{
            "hostid":host_list
        },
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": auth
}

hosts = requests.get(url,headers=header,data=json.dumps(h_json)) 

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
                         "hostid": "%s"%host_dic[i][0],"type": 0,"value_type": 3,"interfaceid": "%s"%host_dic[i][2],"delay": "60s",'history':"7d"},"auth": auth,"id": 1} 
            hosts = requests.get(url,headers=header,data=json.dumps(check_port))                                                                     
                                                                                                                                                     
            trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "%s port %s down"%(app,v),                             
                       "expression": "{%s:net.tcp.listen[%s].max(#3)}=0"%(host_dic[i][1],v),"priority": 3,},],                                       
                       "auth": auth,"id": 4}                                                                                                         
            trig = requests.get(url,headers=header,data=json.dumps(trigger))                                                                         
                                                                                                                                                     
        except :                                                                                                                                     
            print app,v,'supp'                                                                                                                       
            # supp                                                                                                                                   
            check_server = {"jsonrpc": "2.0","method": "item.create","params": {"name": "%s process check"%app,"key_": "proc.num[,,all,%s]"%v,       
                         "hostid": "%s"%host_dic[i][0],"type": 0,"value_type": 3,"interfaceid": "%s"%host_dic[i][2],"delay": "60s",'history':"7d"},"auth": auth,"id": 1} 
            hosts = requests.get(url,headers=header,data=json.dumps(check_server))                                                                   
                                                                                                                                                     
            trigger = {"jsonrpc": "2.0","method": "trigger.create","params": [{"description": "%s process down"%app,                                 
                       "expression": "{%s:proc.num[,,all,%s].max(#3)}=0"%(host_dic[i][1],v),"priority": 3,},],                                       
                       "auth": auth,"id": 4}                                                                                                         
            trig = requests.get(url,headers=header,data=json.dumps(trigger))                                                                         
        print(hosts.json())                                                                                                                          
        print(trig.json())
