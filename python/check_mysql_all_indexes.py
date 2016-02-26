#!/usr/bin/env python
#coding:utf-8
import os
import sys
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

#simple caller, disguard output
def check_all_indexes(host,port,username,password):
	cmd='php /usr/local/lepus/ss_get_mysql_stats.php --host '+host+' --user '+username+' --pass '+password+' --items innodb'
	os.system(cmd)

def main():

    #get mysql servers list
    servers = func.mysql_query('select id,host,port,username,password,tags from db_servers_mysql where is_delete=0 and monitor=1;')

    logger.info("check mysql controller started.")

    if servers:
         plist = []
         for row in servers:
             server_id=row[0]
             host=row[1]
             port=row[2]
             username=row[3]
             password=row[4]
             tags=row[5]
             #thread.start_new_thread(check_mysql, (host,port,user,passwd,server_id,application_id))
             #time.sleep(1)
             p = Process(target = check_all_indexes, args = (host,port,username,password))
             plist.append(p)
         for p in plist:
             p.start()
         time.sleep(10)
         for p in plist:
             p.terminate()
         for p in plist:
             p.join()

    else:
         logger.warning("check mysql: not found any servers")

    logger.info("check mysql controller finished.")


if __name__=='__main__':
    main()

