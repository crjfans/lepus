#!/usr/bin/env python
#coding:utf-8
import os
import sys
import string
import time
import datetime
import MySQLdb
path='./include'
sys.path.insert(0,path)
import functions as func
from multiprocessing import Process;

def check_mysql_variables(host,port,username,password,server_id,tags):
    try:
        conn=MySQLdb.connect(host=host,user=username,passwd=password,port=int(port),connect_timeout=2,charset='utf8')
        curs=conn.cursor()
        conn.select_db('information_schema')
        try:
           global_var=curs.execute("SELECT VARIABLE_NAME,VARIABLE_VALUE FROM GLOBAL_VARIABLES;");
           if global_var:
               for row in curs.fetchall():
                   datalist=[]
                   for r in row:
                      datalist.append(r)
                   result=datalist
                   if result:
                        sql="insert into mysql_variables(server_id,host,port,tags,variable_name,variable_value) values(%s,%s,%s,%s,%s,%s);"
                        param=(server_id,host,port,tags,result[0],result[1])
                        func.mysql_exec(sql,param)
        except :
           pass

        finally:
           curs.close()
           conn.close()
           sys.exit(1)

    except MySQLdb.Error,e:
        pass
        print "Mysql Error %d: %s" %(e.args[0],e.args[1])


def main():
    #get mysql servers list
    func.mysql_exec('truncate table mysql_variables;','')
    servers = func.mysql_query('select id,host,port,username,password,tags from db_servers_mysql where is_delete=0 and monitor=1 and variable_monitor=1;')
    if servers:
        print("%s: check mysql variables controller started." % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),));
        plist = []
        for row in servers:
            server_id=row[0]
            host=row[1]
            port=row[2]
            username=row[3]
            password=row[4]
            tags=row[5]
            p = Process(target = check_mysql_variables, args = (host,port,username,password,server_id,tags))
            plist.append(p)
        for p in plist:
            p.start()
        time.sleep(15)
        for p in plist:
            p.terminate()
        for p in plist:
            p.join()
        func.mysql_exec("insert into mysql_variables_history(server_id,host,port,tags,variable_name,variable_value_old,variable_value_new,create_time) select a.server_id,a.host,a.port,a.tags,a.variable_name,b.variable_value,a.variable_value,a.create_time from mysql_variables a left join mysql_variables_mid b on a.variable_name=b.variable_name and a.host=b.host and a.port=b.port where coalesce(a.variable_value,'')<>coalesce(b.variable_value,'') and b.server_id is not null;",'')
        func.mysql_exec('truncate table mysql_variables_mid;','')
        func.mysql_exec('insert into mysql_variables_mid(server_id,host,port,tags,variable_name,variable_value,create_time) select server_id,host,port,tags,variable_name,variable_value,create_time from mysql_variables;','')
        print("%s: check mysql variables controller finished." % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),))
                     

if __name__=='__main__':
    main()
