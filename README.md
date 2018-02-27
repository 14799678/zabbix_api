# zabbix api
```
会不断完善...

vim conf/port.conf  修改文件可进行监控添加。

[10.86.160.113] 主机ip
flume = 1463    添加端口类型监控
storm = storm.cache.RedisTotalCacheInitUtil 添加进程类型监控

```

# zabbix_api 配置
`settings.py` 修改配置文件内的`地址` `用户名` `密码`<br>

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

## zabbix_jk_values.py

```
可以拿出所有主机的某项监控最后一次数值( item --> key )，并且排序或者字典格式打印。
python zabbix_jk_values.py net.if.in[bond0] show_dic     # 字典格式打印，可以根据需求在自建平台出图等操作。
python zabbix_jk_values.py net.if.in[bond0] show_sort    # value排序 从大到小

```
