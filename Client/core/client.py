#coding=utf-8
import time
from Client.conf import settings
import urllib.request,urllib.error,urllib.parse
import json
import threading
import jsonschema
from plugin import plugin_api



class Client_operation(object):
    def __init__(self):
        self.monitor_service = {}

    '''获取监控配置信息'''
    def load_latest_config(self):
        request_type = settings.config['urls']['get_config'][1]  #判断是get 请求还是post请求
        url = "%s/%s"%(settings.config['urls']['get_config'][0],settings.config['HostID']) #获取请求的url
        latest_configs = self.url_request(request_type,url)
        latest_configs = json.loads(latest_configs)
        self.monitor_service.update(latest_configs)      #将获取到的配置信息保存到字典中


    '''到达监控时间点就获取一次监控配置信息'''
    def run_forever(self):
        '''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''
        flag =False
        config_last_update_time = 0
        while not flag:
            if time.time()-config_last_update_time > settings.config['ConfigUpdateInterval']:              #判断是否达到监控的时间点，并从0开始监控
                self.load_latest_config()     #达到监控时间点就去获取需要监控的参数
                print('load latest config:',self.monitor_service)
                config_last_update_time = time.time()
            for sevice_name,time_value in self.monitor_service['services'].items():
                if len(time_value)==2:    #第二次开始起加上监控的时间
                    self.monitor_service['services']['service_name'].append(0)
                monitor_interval = time_value[1]          #取出监控间隔时间
                latest_interval = time_value[2]
                if time.time()-latest_interval>monitor_interval:
                    print(latest_interval,time.time())
                    self.monitor_service['services']['sevice_name'][2]=time.time()          #更新最新的的监控时间
                    t=threading.Thread(target=self.use_plugin,args=(sevice_name,time_value))   #创建线程
                    t.start()
                    print('start monitor')
                else:
                    print("等待重新获取监控数据")
                time.sleep(1)



    '''将返回的参数值取出'''
    def use_plugin(self,sevice_name,time_value):
        print('开始提取参数')
        plugin_name = time_value[0]
        if hasattr(plugin_api,plugin_name):     #判断plugin_api 中是否有plugin_name
            func = getattr(plugin_api,plugin_name)  #获取plugin_name属性
            plugin_callback =func()
            report_data = {
                'client_id':settings.config['HostID'],
                'service_name':sevice_name,
                'data':json.dumps(plugin_callback)
            }
            request_action = settings.config['urls']['service_report'][1]     #post请求发出
            request_url = settings.config['urls']['service_report'][0]        #url请求地址
            print(report_data)
            self.url_request(request_action,request_url,params=report_data)
        else:
            print('plugins:',time_value)


    '''向服务端发起请求，获取到参数'''
    def url_request(self,type,url,**extra_data):
        real_url = "http://%s:%s/%s"%(settings.config['Server'],settings.config['ServerPort'],url)
        if type in ('get','GET'):
            print(url,extra_data)
            try:
                req = urllib.request.urlopen(real_url,timeout=settings.config['RequestTimeout'])
                callback = req.reade()
                return callback
            except urllib.error as e:
                exit("\033[31;1m%s\033[0m"%e)
        elif type in ('post','POST'):              #将获取到的数据返回给服务器端并画图
            try:
                data_encode = urllib.parse.urlencode(extra_data['params'])
                req = urllib.request.urlopen(url=real_url,data=data_encode,timeout=settings.config['RequestTimeout'])
                callback = json.loads(req.reade())
            except Exception as e:
                print('请求发送失败')
                exit("\033[31;1m%s\033[0m" % e)
