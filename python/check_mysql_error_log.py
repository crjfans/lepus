#!/usr/bin/env python2.7  
#-*- encoding: utf-8 -*-  
  
""" 
该模块用于提取每天mysql日志中的异常或错误信息 
author: xiaomo 
email: moxiaomomo@gmail.com 
"""  
  
import os  
import sys  
import string  
from datetime import *  
  
# 預設字符解碼器為utf-8  
reload(sys)  
sys.setdefaultencoding('utf-8')   
  
COMMON_FLAGS = ["error", "exception", "fail", "crash", "repair"]  
  
def _contain_flag(cur_str):  
    for flag in COMMON_FLAGS:  
        if flag in string.lower(cur_str):  
            return True  
    return False  
  
""" 
获取当前mysql实例的error_log文件路径 
"""  
def _get_mysql_error_log_path():  
    log_path = ''  
    grep_infos = os.popen('ps aux | grep mysql | grep "log-error"').read()  
    if len(grep_infos) > 1:  
        grep_infos = grep_infos.split("log-error=")  
    if len(grep_infos) > 1:  
        grep_infos = grep_infos[1].split(' ')  
    if len(grep_infos) > 1:  
        log_path = grep_infos[0]  
    return log_path  
  
""" 
读取mysql错误日志中包含异常或错误信息的行 
"""  
def _get_error_info(error_log, begin_date):  
    error_infos = []  
    f = open(error_log, 'r')  
    lines = f.readlines()  
    for line in lines:  
        data_array = line.split(' ')  
        if len(data_array) > 0 and len(data_array[0]) == 10:  
            dt_strs = data_array[0].split('-')  
            cur_date = date(int(dt_strs[0]), int(dt_strs[1]), int(dt_strs[2]))  
            if cur_date >= begin_date and _contain_flag(line):  
                error_infos.append(line)  
    f.close()  
    return error_infos  
  
""" 
组装并返回mysql错误日志信息 
"""  
def get_mysql_errors(begin_date=date.today()-timedelta(100)):  
    try:  
        err_log_path = _get_mysql_error_log_path()  
        print err_log_path;
        print begin_date;
        if len(err_log_path) > 1:  
            print _get_error_info(err_log_path, begin_date)  
    except Exception,e:  
        print "[get_mysql_errors]%s"%e     
    return []  

def main():
    get_mysql_errors();
if __name__=='__main__':
    main()
