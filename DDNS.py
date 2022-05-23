'''
DDNS 主程序 使用阿里云的SDK发起请求
Created By caozhg on 2018-11-08
'''
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.acs_exception.exceptions import ClientException
from Utils import Utils
import time

def DDNS():
    client = Utils.getAcsClient()
    recordId = Utils.getRecordId(Utils.getConfigJson().get('Second-level-domain'))
    ip = Utils.getRealIP()
    request = Utils.getCommonRequest()
    request.set_domain('alidns.aliyuncs.com')
    # request.set_version('2018-11-08')
    request.set_action_name('UpdateDomainRecord')
    request.add_query_param('RecordId', recordId)
    request.add_query_param('RR', Utils.getConfigJson().get('Second-level-domain'))
    request.add_query_param('Type', 'A')
    request.add_query_param('Value', ip)
    response = client.do_action_with_exception(request)
    return response

if __name__ == "__main__":
    try:
        while not Utils.isOnline():
            time.sleep(3)
            continue
        print("网络连接成功！")
        result = DDNS()
        print("DDNS解析成功！")
    except (ServerException,ClientException) as reason:
        print("DDNS解析失败！原因为")
        print(reason.get_error_msg())
        print("可参考:https://help.aliyun.com/document_detail/29774.html?spm=a2c4g.11186623.2.20.fDjexq#%E9%94%99%E8%AF%AF%E7%A0%81")
        print("或阿里云帮助文档")