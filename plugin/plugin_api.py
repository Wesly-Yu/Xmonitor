#coding=utf-8
from plugin.linux import cpu,memory,mysql,network,sysinfo,host_alive


'''{"services": {"LinuxCpu": ["LinuxCpuPlugin", 60], "LinuxLoad": ["LinuxLoadPlugin", 60], "LinuxMemery": ["LinuxMemeryPlugin", 60], "Mysql": ["mysql", 60]}}'''

def LinuxCpuPlugin():
    return cpu.cpu_monitor_data()