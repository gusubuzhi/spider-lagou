import requests
import json
import csv
import re
from urllib.parse import urlencode

def get_page(keyworld):
    headers = {
        'Cookie':'_ga=GA1.2.1433680041.1526645158; user_trace_token=20180518200615-dd3a5916-5a93-11e8-b66b-525400f775ce; \
            LGUID=20180518200615-dd3a608d-5a93-11e8-b66b-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGA17EC254BBF200E271DDB33DDF9D0EAD; \
            Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528096807,1528096815,1528096819,1529896059; _gid=GA1.2.1827000249.1529896059; \
            LGSID=20180625110742-ecb72c32-7824-11e8-b04c-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; \
            PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598%3Fpx%3Ddefault%26city%3D%25E6%25B7%25B1%25E5%259C%25B3; \
            index_location_city=%E6%B7%B1%E5%9C%B3; _gat=1; LGRID=20180625110857-19701597-7825-11e8-9759-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529896138; \
            SEARCH_ID=a6f6658a52d542039ac02e0787f5669c',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=new&city=%E6%B7%B1%E5%9C%B3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

    data = {
        'first': 'false',
        'pn': 2,
        'kd': keyworld,
    }
    url = "https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
    res = requests.post(url,data=data,headers = headers)
    data = res.json()
    return data

def get_data_num(data):
    data_num = data['content']['positionResult']['totalCount']
    return data_num

def get_page_data(page,keyworld):
    headers = {
        'Cookie':'_ga=GA1.2.1433680041.1526645158; user_trace_token=20180518200615-dd3a5916-5a93-11e8-b66b-525400f775ce; \
            LGUID=20180518200615-dd3a608d-5a93-11e8-b66b-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGA17EC254BBF200E271DDB33DDF9D0EAD; \
            Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528096807,1528096815,1528096819,1529896059; _gid=GA1.2.1827000249.1529896059; \
            LGSID=20180625110742-ecb72c32-7824-11e8-b04c-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; \
            PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598%3Fpx%3Ddefault%26city%3D%25E6%25B7%25B1%25E5%259C%25B3; \
            index_location_city=%E6%B7%B1%E5%9C%B3; _gat=1; LGRID=20180625110857-19701597-7825-11e8-9759-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529896138; \
            SEARCH_ID=a6f6658a52d542039ac02e0787f5669c',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=new&city=%E6%B7%B1%E5%9C%B3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

    data = {
        'first': 'false',
        'pn': page,
        'kd': keyworld,
    }
    print("--------正在下载第【%d】页--------" %page)
    url = "https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
    res = requests.post(url,data=data,headers = headers)
    data = res.json()
    return data

def pare_data(data):
    itmes = data['content']["positionResult"]['result']
    for itme in itmes:
        yield {
            'positionName': itme['positionName'],
            'workYear':itme['workYear'],
            'education':itme['education'],
            'salary':itme['salary'],
            'financeStage':itme['financeStage'],
            'createTime':itme['createTime'],
            'companySize':itme['companySize'],
            'district':itme['district'],
            'positionLables':itme['positionLables'],
            'businessZones':itme['businessZones'],
            'companyFullName' :itme['companyFullName'],
            'positionId':itme['positionId']
        }

def save_to_csv(itme,keyworld):
    fieldpath = "%s.csv" %keyworld
    with open(fieldpath,'a',newline='') as csvfile:
        fieldname = ['positionName','workYear','education','salary','financeStage','createTime','companySize','district','positionLables','businessZones','companyFullName','positionId']
        writer = csv.DictWriter(csvfile,fieldnames=fieldname)
        if not fieldname:
            writer.writeheader()
        else:
            pass
        for i in itme:
            writer.writerow({'positionName': i['positionName'],
                'workYear':i['workYear'],
                'education':i['education'],
                'salary':i['salary'],
                'financeStage':i['financeStage'],
                'createTime':i['createTime'],
                'companySize':i['companySize'],
                'district':i['district'],
                'positionLables':i['positionLables'],
                'businessZones':i['businessZones'],
                'companyFullName' :i['companyFullName'],
                'positionId':"https://www.lagou.com/jobs/"+str(i['positionId'])+".html",})
        print("保存完毕！！")


def main():
    while True:
        keyworld = input("请输入要搜索的岗位名称>>>")
        start_data = get_page(keyworld)
        data_num =get_data_num(start_data)
        page_num = data_num //15
        print("********一共有【%d】条数据, 共【%d】页********" % (data_num,page_num))
        for page in range(2,page_num+1):
            data = get_page_data(page,keyworld)
            itme=pare_data(data)
            try:
                save_to_csv(itme,keyworld)
            except UnicodeEncodeError:
                pass

if __name__ == "__main__":
    main()

