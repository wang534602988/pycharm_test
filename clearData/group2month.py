import pandas as pd
import numpy as np

HEADER = ['app_name', 'authority', 'releaseDate', 'developer', 'tabName']
goals = ['影音娱乐','实用工具','社交通讯','教育','新闻阅读','拍摄美化','美食','出行导航','旅游住宿','购物比价','商务','儿童','金融理财','运动健康','便捷生活','汽车']

data = pd.read_csv('tabAll.csv',encoding='gbk')
sep = data.shape
head = data.columns
l,h = sep[1],sep[0]
dict = {}
for i in range(6,len(head)):
    dict[head[i]] = 'mean'
goal1 = data.groupby(['mt']).agg(dict)
goal1.to_csv('mouth.csv',encoding='gbk')
print('success')