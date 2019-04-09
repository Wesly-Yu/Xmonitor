#coding=utf-8
from plugin.linux import cpu,memory,mysql,network,sysinfo,host_alive

'''通过反射执行'''
'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''

def LinuxCpuPlugin():
    return cpu.cpu_monitor_data()



def LinuxMemery():
    return memory