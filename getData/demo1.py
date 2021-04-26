import requests
import json
import csv
import codecs

HEADER = ['app_name', 'authority', 'releaseDate', 'developer', 'tabName']
MAX_COUNT = 100
goals = ['影音娱乐','实用工具','社交通讯','教育','新闻阅读','拍摄美化','美食','出行导航','旅游住宿','购物比价','商务','儿童','金融理财','运动健康','便捷生活','汽车']
goal = goals[15]
# 获取uri 即每个分类的标识
def get_uri():
    fujia = '0b58fb4b937049739b13b6bb7c38fd53'
    tab = {}
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
            tabName = k.get('tabName')
            if tabName == goal:
                aim = tab_ids[0]
                tab_id = aim.get('tabId')
                result.append(tab_id)
                for e in tab_ids:
                    tab_id1 = e.get('tabId')
                    if tab_id1 not in result:
                        tab[tab_id1] = tabName
                        all_tab_uri.append(tab_id1)
        all_tab_uri.append(fujia)
    return tab


# 获取每个分类里应用的appid
def get_appid(uri, tabName):
    tabName = tabName
    n = 1
    # 死循环，当layoutData为空时，停止获取appid，即一个类别爬取结束
    while True:
        url = f'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={n}&uri={uri}&maxResults=250&zone=&locale=zh_CN'
        r = requests.get(url)
        _json = json.loads(r.text)
        data1 = _json.get('layoutData')
        if len(data1) != 0:
            for i in range(0,MAX_COUNT):
                try:
                    app = data1[i]
                    datalist = app.get('dataList')
                    for data in datalist:
                        appid = data.get('appid')
                        yield appid, tabName
                except:
                    pass
            n += 1
        else:
            break


def parse(appid, tabName):
    item = {}
    url = f'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&maxResults=25&uri=app%7C{appid}&shareTo=&currentUrl=https%253A%252F%252Fappgallery.huawei.com%252F%2523%252Fapp%252F{appid}&accessId=&appid={appid}&zone=&locale=zh_CN'
    headers = {
        'Connection': 'close'
    }
    r = requests.get(url,headers =headers)
    r.encoding = 'utf-8'
    _json = json.loads(r.text)
    data = _json.get('layoutData')
    aim_appname = data[1]
    datalist1 = aim_appname.get('dataList')
    for data1 in datalist1:
        item['app_name'] = data1.get('name')
    aty = str(getItem('authority', data)['list'][0]['text'])
    aty = aty.replace('\\n', '')
    aty = aty.replace('.', '')
    item['authority'] = aty
    item['developer'] = getItem('developer', data)
    item['releaseDate'] = getItem('releaseDate', data)
    item['tabName'] = tabName
    print(tabName)
    # 将得到的数据插入到数据 使用insert方法（先将数据转为字典类型）
    data = dict(item)
    if data:
        return data


def getItem(item, data):
    content = ''
    for i in range(0, 11):
        content = look(i, data, item)
        if content:
            break
    return content


def look(order, data, item):
    flag = data[order]
    datalist = flag.get('dataList')
    for data in datalist:
        app_intro = data.get(item)
        if app_intro:
            return app_intro
        else:
            return False


with codecs.open('app.csv', 'a+') as csvfile:
    fieldnames = HEADER
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    tab = get_uri()
    for url in tab.keys():
        for appid, tabName in get_appid(url, tab[url]):
            try:
                writer.writerow(parse(appid, tabName))
            except:
                print('cant write')

print(f'\033[31;44m********************程序结束了********************\033[0m')

