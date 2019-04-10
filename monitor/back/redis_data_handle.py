#coding=utf-8

from  django.conf import settings
import time,json
import copy


class DataStore(object):

    def __init__(self,client_id,service_name,data,redis_obj):
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.redis_conn_obj = redis_obj
        # self.process_save()


    # def process_save(self):


