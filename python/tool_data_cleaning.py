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


def delete_history_data(table_name,expire_days):
    func.mysql_exec('CREATE TABLE '+table_name+'_clean_temp AS SELECT * FROM '+table_name+' WHERE create_time >= from_unixtime(unix_timestamp(now())-('+expire_days+'*24*60*60));','')
    func.mysql_exec('TRUNCATE TABLE '+table_name,'')
    func.mysql_exec('INSERT INTO '+table_name+' SELECT * FROM '+table_name+'_clean_temp','')
    func.mysql_exec('DROP TABLE IF EXISTS '+table_name+'_clean_temp;','')
def main():
    delete_table_list = ['mysql_status_history',\
                         'mysql_bigtable_history',\
                         'mysql_status_extend',\
                         'mysql_replication_history',\
                         'mysql_connected',\
                         'alarm_history']
    expire_days='7'
    print "start to clean the data of history tables"
    try:
	for table_name in delete_table_list:
            delete_history_data(table_name,expire_days)
        print "successfully clean the data of history tables"
    except Exception, e:
        print e
        sys.exit(1)

    finally:
        sys.exit(1)


if __name__=='__main__':
    main()
