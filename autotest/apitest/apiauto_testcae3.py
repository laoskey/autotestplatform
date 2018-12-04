# -*- coding:utf-8 -*-
import requests ,time, sys, re
import urllib, zlib
import pymysql
import json
from trace import CoverageResults
from idlelib.rpc import response_queue
from time import sleep

HOSTNAME = '217.0.0.1'

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
        interfaceTest（case_list）
    coon.commit()
    cursor.close()
    coon.close()

def interfaceTest(case_list):
    res_flag = []
    request_urls = []
    response = []
    strinfo = re.compile('{TaskId}')
    strinfo1 = re.compile('{AssertId}')
    strinfo2 = re.compile('{PointId}')
    assertinfo = re.compile('{assertno}')
    tasknoinfo = re.compile('{taskno}')
    schemainfo = re.compile('{schema}')
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            method = case[3]
            url = case[2]
            param =case[4]
            res_check = case[5]

        except Exception as e:
            return '测试用例格式不对%s'%e

        if param == '':
            new_url = 'http://'+'api.test.com.cn'+url

        elif param == 'null':
            new_url = 'http://'+url

        else:
            url = strinfo.sub(TaskId, url)
            param = strinfo.sub(TaskId, param)
            param = tasknoinfo.sub(taskno,param)
            new_url = 'http://'+'127.0.0.1'+'url'
            request_urls.append(new_url)

        if method.upper() == 'GET':
            headers = {'Authorization': '','Content-Type': 'application/json'}
            if '=' in urlParam(param):
                data = None
                print(str(case_id)+'request is get'
                      +str(new_url.encode('utf-8'))+'?'+urlParam(param).encode('utf-8'))

                results = requests.get(new_url+'?'=urlParam(param), data, headers=headers).text
                print('response is get'+ results.encode('utf8'))
                response.append(requests,'')
            else:
                print('results is get'+new_url+'body is '+urlParam(param))
                data = None
                req = urllib.request.Request(url=new_url, data=data, headers=headers, method='GET')
                results = urllib.requset.urlopen(req).read()
                print('response is get ')
                print(results)
                res = readRes(results,res_check)

            if 'pass' == res:
                writeResult(case_id, '1')
                res_flag.append('pass')
            else:
                res_flag.append('fail')
                writeResult(case_id, '0')
        if method.upper() == "PUT":
            headers = {'Host':HOSTNAME,'Connection': 'keep-live', 'CredentialId': id,
                       'Content-Type': 'application/json'}
            body_data = param
            results = requests.put(url=url,data=body_data,headers=headers)
            response.append(results)
            res = readRes(results, res_check)
            if 'pass' == res:
                writeResult(case_id, 'pass')
                res_flag.append('pass')

            else:
                res_flag.append('fail')
                writeResult(case_id, 'fail')
