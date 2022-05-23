'''
AcsClient的单实例类
created by caozhg on 2018-11-08
'''
from aliyunsdkcore.client import AcsClient
import Utils as tools
class AcsClientSing:
    __client = None

    @classmethod
    def getInstance(self):
        if self.__client is None:
            acsDict = tools.Utils.getConfigJson()
            self.__client = AcsClient(acsDict.get('AccessKeyId'), acsDict.get('AccessKeySecret'), 'cn-hangzhou')
        return self.__client