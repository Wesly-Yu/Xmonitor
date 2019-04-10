#coding=utf-8

import redis

def redis_conn(django_settings):
    pool = redis.ConnectionPool(host=django_settings.REDIS_CONN['HOST'], port=django_settings.REDIS_CONN['PORT'],db=django_settings.REDIS_CONN['DB'])
    r = redis.Redis(connection_pool=pool)
    return  r