#提取authority数据，并分割为新的属性值
import pandas as pd
import re
data = pd.read_csv('app.csv',encoding='gbk')
sap = data.shape
h = sap[0]
print(h)
atys = data['authority']
satys = ''
for line in atys:
    satys += line
satys = satys.replace('\n', '')
satys = satys.replace('\\', '')
satys = satys.replace('\r', '')
satys = satys.replace('.', '')
satys = satys.replace(' ', '')
satys = satys.replace(',', '')
authority = []
for i in range(1, 50):
    beg = satys.find(str(i))
    end = satys.find(str(i + 1))
    if beg != -1 and end != -1:
        newAuthority = satys[beg + 1:end]
        newAuthority = newAuthority.replace("0", '')
        newAuthority = newAuthority.replace("1", '')
        newAuthority = newAuthority.replace("2", '')
        newAuthority = newAuthority.replace("3", '')
        newAuthority = newAuthority.replace("4", '')
        newAuthority = newAuthority.replace("5", '')
        newAuthority = newAuthority.replace("6", '')
        newAuthority = newAuthority.replace("7", '')
        newAuthority = newAuthority.replace("8", '')
        newAuthority = newAuthority.replace("9", '')
        authority.append(newAuthority)
        authority = list(tuple(authority))
for item in authority:
    data[item] = [0]*h
    for i in range(0,h):
        if re.search(item, atys[i]) is not None:
            data[item].loc[i]=1
data.to_csv('finApp.csv',encoding='gbk')