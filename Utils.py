'''
工具类
Created By caozhg on 20181108
'''
import re
from bs4 import BeautifulSoup
from urllib import request
import platform
import  subprocess
import json
from AcsClientSingleton import AcsClientSing
from CommonRequestSingleton import CommonRequestSing
class Utils:

    #获取真实公网IP
    def getRealIP():
        url = Utils.getRealUrl();
        ip = Utils.getRealIp(url)
        return ip

    #获取二级域名的RecordId
    def getRecordId(domain):
        client = Utils.getAcsClient()
        request = Utils.getCommonRequest()
        request.set_domain('alidns.aliyuncs.com')
        request.set_version('2018-10-08')
        request.set_action_name('DescribeDomainRecords')
        request.add_query_param('DomainName', Utils.getConfigJson().get('First-level-domain'))
        response = client.do_action_with_exception(request)
        jsonObj = json.loads(response.decode("UTF-8"))
        records = jsonObj["DomainRecords"]["Record"]
        for each in records:
            if each["RR"] == domain:
                return each["RecordId"]

    #获取CommonRequest
    def getCommonRequest():
        return CommonRequestSing.getInstance()

    #获取AcsClient
    def getAcsClient():
        return AcsClientSing.getInstance()

    #获取操作系统平台
    def getOpeningSystem():
        return platform.system()

    #判断是否联网
    def isOnline():
        userOs = Utils.getOpeningSystem()
        try:
            if userOs == "Windows":
                subprocess.check_call(["ping", "-n", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            else:
                subprocess.check_call(["ping", "-c", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            print("网络未连通！请检查网络")
            return False

    #从ip138爬取探测用户实际ip的网页
    def getRealUrl():
        url = r'http://www.ip138.com/'
        # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
        soup = BeautifulSoup(Utils.getPage(url), 'html.parser')
        #获取真实ip
        realUrl = soup.find_all('iframe')[0].get('src')
        return realUrl

    #解析网页，正则判断，获取用户实际公网ip
    def getRealIp(url):
        html = Utils.getPage(url)
        pattern = r"(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)"
        matchs = re.search(pattern, html)
        ip_addr = ""
        for i in range(1,5):
            ip_addr += matchs.group(i) + "."
        return ip_addr[:-1]


    # 模拟真实浏览器进行访问
    def getPage(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        page = request.Request(url, headers=headers)
        page_info = request.urlopen(page).read().decode("gb2312")
        return page_info

    #从config.json中获取配置信息JSON串
    def getConfigJson():
        with open('config.json') as file:
            jsonStr = json.loads(file.read())
        return jsonStr