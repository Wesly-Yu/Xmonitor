#coding=utf-8

from  django.conf import settings
import time,json
import copy




'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''
'''数据格式：[{'idle':'98.60','nice':'0','user':'0.69','system':'1.38','status':'0'},1496571177.3680441]'''
class DataStore(object):

    def __init__(self,client_id,service_name,data,redis_obj):
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.redis_conn_obj = redis_obj
        self.process_save()

    def slice_data(self,latest_data_key,time_interval):
        all_real_data = self.redis_conn_obj.lrange(latest_data_key,1,-1)
        data_set = []         #保存筛选的数据
        for item in all_real_data:
            data = json.loads(item.decode())
            if len(data)==2:
                service_data,last_save_time = data
                if time.time() - last_save_time <= time_interval:
                    data_set.append(data)
                else:
                    pass
        return data_set

    def process_save(self):
        if self.data['status'] ==0:                 #status=0 表示online
            for key,data_series_val in settings.STATUS_DATA_OPTIMIZATION.items():
                data_interval,max_lenth =data_series_val
                data_series_key_in_redis = "StatusData_%s_%s_%s"  %(self.client_id,self.service_name,key)
                last_point_from_redis = self.redis_conn_obj.lrange(data_series_key_in_redis,-1,-1)       #取出最后一个点的值
                if not last_point_from_redis:
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([None,time.time()]))    #第一次没有值时，自行初始化一个时间，为当前的时间戳
                if data_interval == 0:
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([self.data,time.time()]))      #表示是latest数据，只需要保存就行了
                else:
                    last_point_data,last_point_data_time = json.loads(self.redis_conn_obj.lrange(data_series_key_in_redis,-1,-1)[0].decode()) #lrang取出的值是一个列表
                    if time.time() - last_point_data_time >= data_interval:       #如果当前时间减去最后的存储时间大于间隔，则去掉多余的数据
                        latest_data_key_in_redis = "StatusData_%s_%s_latest" %(self.client_id,self.service_name)
                        print('')
                        #把最近n分钟的数据取到，保存到data_set里面
                        data_set = self.slice_data(latest_data_key_in_redis,data_interval)
                        if len(data_set)>0:
                            optimized_data = self.get_optimized_data(data_series_key_in_redis,data_set)         #计算优化结果
                            if optimized_data:
                                self.save_optimized_data(data_series_key_in_redis,optimized_data)      #将优化的结果调用保存的  函数 保存到redis
                if self.redis_conn_obj.llen(data_series_key_in_redis)>= max_lenth:
                    self.redis_conn_obj.lpop(data_series_key_in_redis)
        else:
            print("report data is valid:",self.data)
            raise ValueError

    def get_optimized_data(self,data_set_key,raw_service_data):
        '''计算服务端各种数据的平均值，最大值，中位数，最小值'''
        print('get_optimized_data:', raw_service_data[0])
        service_data_keys = raw_service_data[0][0].keys()
        optimizes_dic = {}   #保存优化后的数据
        for key in service_data_keys:
            optimizes_dic[key] = []
            temporary_data_dict = copy.deepcopy(optimizes_dic)          #将数据复制出来进行计算，避免影响原始数据
            for service_data_item,last_save_time in raw_service_data:
                for service_index,v in service_data_item.items():
                    try:
                        temporary_data_dict[service_index].append(round(float(v),2))    #把指标名和值存储到列表中{idele:[80,90,98,70]}
                    except ValueError as e:
                        pass
                for service_key,v_list in temporary_data_dict.items():
                    avg_data = self.get_average(v_list)
                    max_data = self.get_max(v_list)
                    min_data = self.get_min(v_list)
                    mid_data = self.get_mid(v_list)
                    optimizes_dic[service_key]=[avg_data,max_data,min_data,mid_data]
                    print(service_key,optimizes_dic[service_key])



    def save_optimized_data(self,data_series_key_in_redis,optimized_data):
        '''将优化后的数据保存到redis'''
        print('保存数据到redis库')
        self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([optimized_data,time.time()]))


    def get_average(self,data_dict):
        '''求平均值'''
        if len(data_dict)>0:
            return round(sum(data_dict)/len(data_dict),2)
        else:
            return 0
    def get_max(self,data_dict):
        '''求最大值'''
        if len(data_dict)>0:
            return max(data_dict)
        else:
            return 0

    def get_min(self,data_dict):
        '''求最小值'''
        if len(data_dict) > 0:
            return min(data_dict)
        else:
            return 0
    def get_mid(self,data_dict):
        '''求中值'''
        data_dict.sort()
        if len(data_dict)>0:
            return data_dict[int(len(data_dict)/2)]
        else:
            return 0