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
from apitest.apitest_test_method import interfaceTest
import unittest


HOSTNAME = '127.0.0.1'


class Apiflow(unittest.TestCase):
    """登陆制服接口流程"""
    def setUp(self):
        time.sleep(1)

    def test_readSQLcase(self):
        try:
            sql = "SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiresult, apistatus FROM apitest_apistep WHERE apitest_apistep.Apitest_id=2"

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
                interfaceTest(case_list)
            coon.commit()
            cursor.close()
            coon.close()
        except:
            print("执行数据库语句出错，错误语句是%s"%sql)

    def tearDown(self):
        time.sleep(1)


if __name__ == "__main__":
    import HTMLTestRunner
    import os
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(Apiflow("test_readSQLcase"))

    filename = "%s\\templates\\apitest_report.html"%os.getcwd()
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="流程接口测试报告", description=u"流程场景接口")
    runner.run(testunit)








