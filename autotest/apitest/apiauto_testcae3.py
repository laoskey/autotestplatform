# -*- coding:utf-8 -*-
import requests ,time, sys, re
import urllib, zlib
import pymysql
import json
from trace import CoverageResults
from idlelib.rpc import response_queue
from time import sleep
from apitest.apitest_test_method import readRes, urlParam, CredentialId
from apitest.apitest_test_method import preOrderSN, TaskId, taskno
from apitest.apitest_test_method import writeBug, writeResult

HOSTNAME = '127.0.0.1'

def readSQLcase():
    sql = "SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiresult, apistatus"\
          "FROM apitest_apistep WHERE apitest_apistep.Apitest_id=3"
    coon = pymysql.connect(
        user='root',
        passwd='test123456',
        db='autotest',
        port=3306,
        host='127.0.0.1',
        charset='utf8',
    )
    cursor = coon.cursor()
    aa = cursor.execute(sql)
    info = cursor.fetchmany(aa)
    for ii in info:
        case_list = []
        case_list.append(ii)
        # CredentialId()
        # interfaceTest（case_list）
    coon.commit()
    cursor.close()
    coon.close()


if __name__ == '__main__':
    readSQLcase()
    print('Done')
    time.sleep(1)




