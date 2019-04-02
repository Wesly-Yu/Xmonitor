#coding=utf-8
config ={
    'HostID':1,
    'Server':"localhost",
    'ServerPort':8090,
    'urls':{
        'get_config':['api/client/config','get'],
        'service_report':['api/client/service/report/','post'],
    },
    'RequestTimeout':30,
    'ConfigUpdateInterval':300,
}