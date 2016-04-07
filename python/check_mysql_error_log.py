#!/usr/bin/env python
#coding:utf-8
import os
import sys
import paramiko
import string
import time
import datetime
import MySQLdb
import logging
import logging.config
logging.config.fileConfig("etc/logger.ini")
logger = logging.getLogger("lepus")
path='./include'
sys.path.insert(0,path)
import functions as func
import lepus_mysql as mysql
from multiprocessing import Process;


def get_errors(ssh_host,ssh_port,ssh_user,ssh_passwd,last_line_num):
    error_log_path=''
    total_num=0
    error_msg=[]
    error_msg_arr={}
    line_num=0
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ssh_host, ssh_port, username=ssh_user, password=ssh_passwd, timeout=10)
    except Exception, e:
        logger.error(str(e).strip('\n'))
        sys.exit(1)
    try:
        #get error log path
        stdin, stdout, stderr = client.exec_command("ps aux | grep mysql | grep 'log-error=' | grep -v 'grep' | awk -F'log-error=' '{print $2}' | awk '{print $1}'")
        for log_path in stdout.readlines():
            error_log_path=str(log_path).strip('\n')
        if error_log_path.strip()=='':
            return False
        #get total line number of error log
        stdin, stdout, stderr = client.exec_command("wc -l "+error_log_path+" | awk '{print $1}'")
        for std in stdout.readlines():
            total_num=str(std).strip('\n')
        if int(total_num)<=0:
            return False
        #get line number for tail command
        line_num=int(total_num)-int(last_line_num)
        if int(line_num)<=0:
            return False
        stdin, stdout, stderr = client.exec_command('tail -n '+str(line_num)+' '+error_log_path+' |egrep -i "warning|error" ')
        for msg in stdout.readlines():
            error_msg.append(msg)
    except Exception, e:
        logger.error(str(e).strip('\n'))
        sys.exit(1)
    finally:
        client.close()
    error_msg_arr['msg']=error_msg
    error_msg_arr['total_num']=total_num
    return error_msg_arr

def insert_errors_to_table(ssh_host,ssh_port,ssh_user,ssh_passwd,last_line_num,server_port,tags,server_id):
    try:
        host = func.get_config('monitor_server','host')
        port = func.get_config('monitor_server','port')
        user = func.get_config('monitor_server','user')
        passwd = func.get_config('monitor_server','passwd')
        dbname = func.get_config('monitor_server','dbname')
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=10,charset='utf8')
        conn.select_db(dbname)
        curs = conn.cursor()
    except Exception,e:
        logger.error(str(e).strip('\n'))
        sys.exit(1)
    try:
        error_msg_arr=get_errors(ssh_host,ssh_port,ssh_user,ssh_passwd,last_line_num)
        if error_msg_arr==False:
            return
        for msg in error_msg_arr['msg']:
            msg=msg.strip('\n')
            if msg.upper().find('WARNING')>0:
                error_level=1
            else:
                error_level=2
            sql="insert into mysql_check_error_log(server_id,host,port,tags,error_level,error_event) values (%s,%s,%s,%s,%s,%s);"
            param=(server_id,ssh_host,server_port,tags,error_level,msg)
            curs.execute(sql,param)
        conn.commit()
        sql="update db_servers_mysql set error_log_monitor_last_line_num=%s where id=%s;"
        param=(error_msg_arr['total_num'],server_id)
        curs.execute(sql,param)
        conn.commit()
    except Exception, e:
        logger.error(str(e).strip('\n'))
        sys.exit(1)
    finally:
        conn.commit()
        curs.close()
        conn.close()

def main():

    #get mysql servers list
    servers = func.mysql_query("select id,host,port,username,password,tags,ssh_user,ssh_port,ssh_passwd,error_log_monitor_last_line_num\
                                from db_servers_mysql where is_delete=0 and monitor=1 and error_log_monitor=1;")

    logger.info("check mysql error log started.")

    if servers:
         plist = []
         for row in servers:
             server_id=row[0]
             host=row[1]
             port=row[2]
             username=row[3]
             password=row[4]
             tags=row[5]
             ssh_user=row[6]
             ssh_port=row[7]
             ssh_passwd=row[8]
             error_log_monitor_last_line_num=row[9]
             p = Process(target = insert_errors_to_table, args = (host,ssh_port,ssh_user,ssh_passwd,error_log_monitor_last_line_num,port,tags,server_id))
             plist.append(p)
         for p in plist:
             p.start()
         time.sleep(20)
         for p in plist:
             p.terminate()
         for p in plist:
             p.join()

    else:
         logger.warning("check mysql: not found any servers")

    logger.info("check mysql error log finished.")


if __name__=='__main__':
    main()
