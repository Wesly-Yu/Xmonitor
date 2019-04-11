#coding=utf-8

from  django.conf import settings
import time,json
import copy




'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''
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
        if self.data['status'] ==0:
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
                                self.save_optimized_data(data_series_key_in_redis,optimized_data)


    def get_optimized_data(self,data_set_key,raw_service_data):
        '''计算服务端各种数据的平均值，最大值，中位数，最小值'''
        print('get_optimized_data:', raw_service_data[0])



    def save_optimized_data(self,data_series_key_in_redis,optimized_data):
        '''保存数据到redis'''
        print('保存数据到redis库')



