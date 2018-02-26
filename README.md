# zabbix api
```
会不断完善...

vim conf/port.conf  修改文件可进行监控添加。

[10.86.160.113] 主机ip
flume = 1463    添加端口类型监控
storm = storm.cache.RedisTotalCacheInitUtil 添加进程类型监控

```

# zabbix配置
`settings.py` 修改配置文件<br>

----

## zabbix_group_jk.py

```
脚本跟参数，参数是zabbix组内的名称。针对某一个组内的ip来添加监控项。
```


## zabbix_jk.py

```
通过修改脚本内部参数，针对所有主机ip添加监控项。
```

## zabbix_item_rename.py

```
修改主机的监控项目名称与删除。

```
