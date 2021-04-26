import requests
import json
import random
from concurrent.futures import ThreadPoolExecutor
import pymongo

class HuaWei_appPrase(object):
    def __init__(self):
        # MONGODB 主机名
        host = "127.0.0.1"
        # MONGODB 端口号
        port = 27017
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        dbname='HuaWei'
        sheetname='HuaWei_apps'
        mydb = client[dbname]
        self.post = mydb[sheetname]
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    #获取uri 即每个分类的标识
    def get_uri(self):
        fujia = '0b58fb4b937049739b13b6bb7c38fd53'
        all_tab_uri = list()
        result = list()
        for i in range(2):
            if i == 0:
                url = 'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri=b2b4752f0a524fe5ad900870f88c11ed&maxResults=25&zone=&locale=zh_CN'
            else:
                url = 'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri=56a37d6c494545f98aace3da717845b7&maxResults=25&zone=&locale=zh_CN'
            r = requests.get(url)
            _json = json.loads(r.text)
            data = _json.get('tabInfo')
            for k in data:
                tab_ids = k.get('tabInfo')
                aim = tab_ids[0]
                tab_id = aim.get('tabId')
                result.append(tab_id)
                for e in tab_ids:
                    tab_id1 = e.get('tabId')
                    if tab_id1 not in result:
                        all_tab_uri.append(tab_id1)
            all_tab_uri.append(fujia)
        return all_tab_uri

    #获取每个分类里应用的appid
    def get_appid(self,uri):
        n=1
        #死循环，当layoutData为空时，停止获取appid，即一个类别爬取结束
        while True:
            url=f'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={n}&uri={uri}&maxResults=250&zone=&locale=zh_CN'
            r=requests.get(url,headers=self.headers)
            _json=json.loads(r.text)
            data1=_json.get('layoutData')
            if len(data1)!=0:
                for app in data1:
                    datalist=app.get('dataList')
                    for data in datalist:
                        appid=data.get('appid')
                        yield appid
                n += 1
            else:
                break

    #解析主程序，用于解析每个app的name和introduce
    def parse(self,appid):
        item={}
        url=f'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&maxResults=25&uri=app%7C{appid}&shareTo=&currentUrl=https%253A%252F%252Fappgallery.huawei.com%252F%2523%252Fapp%252F{appid}&accessId=&appid={appid}&zone=&locale=zh_CN'
        r=requests.get(url,headers=self.headers)
        r.encoding='utf-8'
        _json=json.loads(r.text)
        data=_json.get('layoutData')
        aim_appname=data[1]
        datalist1=aim_appname.get('dataList')
        for data1 in datalist1:
            item['app_name']=data1.get('name')
        #通过分析发现 app_intro 在dataList里面 但是有的在[6] 有的在[7]，所以要加判断
        flag1=data[7]
        datalist=flag1.get('dataList')
        for data2 in datalist:
            app_intro=data2.get('appIntro')
            if app_intro :
                item['app_intro'] = app_intro.replace('\n','').replace('\r','').replace('\t','')
            else:
                flag2 = data[6]
                datalist2 = flag2.get('dataList')
                for data2 in datalist2:
                    app_intro2 = data2.get('appIntro')
                    item['app_intro']=app_intro2.replace('\n','').replace('\r','').replace('\t','')
        #将得到的数据插入到数据 使用insert方法（先将数据转为字典类型）
        data=dict(item)
        if data:
        	#在入库前判断是都存在此item（根据item出现次数判断）
            data_count = self.post.count_documents(item)
            if data_count == 0:
                self.post.insert(data)
                print(f'\033[30;46m{item}\033[0m')



#主函数
def main():
    #线程池，创建四个线程
    pool=ThreadPoolExecutor(max_workers=4)
    huaweiapp_prase=HuaWei_appPrase()
    for uri in huaweiapp_prase.get_uri():
        for appid in huaweiapp_prase.get_appid(uri):
            pool.submit(huaweiapp_prase.parse,appid)
    pool.shutdown()
    print(f'\033[31;44m********************程序结束了********************\033[0m')


if __name__ == '__main__':
    main()