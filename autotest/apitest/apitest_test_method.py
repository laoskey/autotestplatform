# -*- coding:utf-8 -*-
import requests ,time, sys, re
import urllib, zlib
import pymysql
import json



def readRes(res,res_check):
    res = res.decode().replace('":', "=").replace('":', "=")
    res_check = res_check.split(';')
    for s in res:
        if s in res:
            pass
        else:
            return '错误，返回参数与预期结果不一致' + s
    return 'pass'


def urlParam(param):
    paraml = param.replace('&quot', '"')
    return paraml


def CredentialId():
    global id
    url = 'http://'+'api.test.com.cn'+'/api/Security/Authentication/Signin/web'
    body_data = json.dumps({"Identity": 'test',"Password": 'test'})
    headers = {'Connection': 'keep-live', 'Content-Type': 'application/json'}
    response = requests.post(url=url, data=body_data, headers=headers)
    data = response.text
    regx = '.*"CredientId":"(.*)","Scene"'
    pm = re.search(regx, data)
    id = pm.group(1)


def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx, results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False


def TaskId(results):
    global TaskId
    regx = '.*"TaskId":"(.*)","PlanId"'
    pm = re.search(regx, results)
    if pm:
        TaskId = pm.group(1).encode('utf-8')
        return TaskId
    return False


def taskno(param):
    global taskno
    a = int(time.time())
    taskno ='task'+str(a)
    return taskno


def writeResult(case_id,result):
    result = result.endcode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE apitest_apistep set apitest_apistep.aplstatus=%s WHERE apitest_apistep.Apitest_id=%s"
    param = (result, case_id)
    print('api autptest result is'+result.endcode())
    coon = pymysql.connect(
        user='root',
        passwd='test123456',
        db='autotest',
        port=3306,
        host='127.0.0.1',
        charset='utf8'
    )
    cursor = coon.cursor()
    cursor.execute(sql, param)
    coon.commit()
    cursor.close()
    coon.close()


def writeBug(bug_id, interface_name, request, response, res_check):
    interface_name = interface_name.encode('utf-8')
    res_check = res_check.encode('utf-8')
    now =time.time("%Y-%m-%d %H:%M:%S")
    bugname = str(bug_id)+'_'+interface_name.decode()+'错错了'
    bugdetail = '[请求数据]<br/>'+request.decode()+'<br/>'+'[预期结果]<br/>'\
                +res_check.decode()+'<br/>'+'<br/>'+'[响应数据]<br/>'+'<br/>'\
                +response.decode()
    print(bugdetail)
    sql = "INSERT INTO  bug_bug (bugname, bugdetail, bugstatus, buglevel, bugcreater, bugassign , create_time, Product_id )" \
          "VALUES ('%s', '%s','1','1','P先生', 'P先生', '%s','2')"%(bugname, pymysql.escape_string(bugdetail),now)
    coon = pymysql.connect(
        user='root',
        passwd='test123456',
        db='autotest',
        port=3306,
        host='127.0.0.1',
        charset='utf8'
    )
    cursor = coon.cursor()
    cursor.execute(sql)
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

                results = requests.get(new_url+'?'+urlParam(param), data, headers=headers).text
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
            headers = {'Host':'127.0.0.1','Connection': 'keep-live', 'CredentialId': id,
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
        writeBug(bug_id=case_id,interface_name=interface_name,
                 request=new_url, response=results,res_check= res_check)
        try:
            preOrderSN(results)
        except:
            print('OK')
        if method.upper() == 'PATCH':
            headers = {'Authorization':'Credential'+id,'Content-Type':'application/json'}
            data = None
            results= requests.patch(new_url+'?'+urlParam(param), data, headers=headers).text
            response.append(results)
            res = readRes(results,res_check)
            if 'pass' == res:
                writeResult(case_id,'pass')
                res_flag.append('pass')
            else:
                res_flag.append('fail')
                writeResult(case_id,'fail')
                writeBug(case_id,interface_name,results,res_check)

            try:
                preOrderSN(results)
            except:
                print('OK')
        if method.upper()=='POST':
            headers = {'Authorization':'Credential'+id,'Content-Type':'application/json'}
            if '=' in urlParam(param):
                data = None
                results = requests.patch(new_url+'?'+urlParam(param), data, headers=headers).text
                print('response is port'+results.encode('utf-8'))
                response.append(results)
                res = readRes(results,'')
            else:
                print(str(case_id)+'request is '+new_url.encode('utf-8')+
                      ' body is '+urlParam(param).encode('utf-8'))
                results = requests.post(new_url, data=urlParam(param).encode('utf-8'), headers=headers).text
                print(' response is post'+results.encode('utf-8'))
                response.append(results,res_check)
                if 'pass' == res:
                    writeResult(case_id,'1')
                    res_flag.append('pass')
                else:
                    res_flag.append('fail')
                    writeResult(case_id,'0')
        writeBug(bug_id=case_id,interface_name=interface_name,
                 request=new_url, response=results,res_check= res_check)

        try:
            TaskId(results)
        except:
            print('OK1')
