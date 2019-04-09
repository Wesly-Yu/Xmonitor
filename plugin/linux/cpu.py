#coding=utf-8

__author__ = 'Wesley-YU'
import subprocess
#常用编码
GBK='gbk'
UTF8='utf-8'
current_encoding =UTF8
#invoke='反射'




def cpu_monitor_data(first_invoke=1):
    shell_commend = 'sar 1 3| grep "^Average:"'
    value_dict = {}
    result_str = subprocess.Popen(shell_commend,shell=True,stdout=subprocess.PIPE).stdout.read()
    value_dict={
        'cpu_monitor':result_str,
        'status':0
    }
    result_str = str(result_str)
    return result_str




if __name__ =='__main__':
    print(cpu_monitor_data())