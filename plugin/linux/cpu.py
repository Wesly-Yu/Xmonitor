#coding=utf-8
import subprocess
#常用编码
GBK='gbk'
UTF8='utf-8'
current_encoding =GBK





def cpu_monitor_data():
    # shell_commend = 'sar 1 3| grep "^Average:"'
    shell_commend = 'ipconfig'
    result_str = subprocess.Popen(shell_commend,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=1)
    while result_str.poll() is  None:
        results = result_str.stdout.readlines()
        return results




if __name__ =='__main__':
    print(cpu_monitor_data())