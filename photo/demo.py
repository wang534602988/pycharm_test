import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Pie

df = pd.read_csv('G:/PythonFIle/appRank/clearData/tabName.csv', encoding='gbk')
sep = df.shape
l, h = sep[1], sep[0]
print(l, h)
ys = []
x = []
time = []
head = df.columns
for i in range(0, l - 1):
    x.append(head[i + 1])
for i in range(0, h):
    y = df.iloc[i][1:].tolist()
    y2 = map(lambda x: int(x), y)
    ys.append(list(y2))
    time.append(df.iloc[i][0])
tl = Timeline()
i=1
data_pair = [list(z) for z in zip(x, ys[i])]
a = [39,16,61,100,0,98,13,12,64,80,99,96,0,0,26,13,78,2,52]
print(ys[i],type(ys[i]))
bar = (
    Bar()
        .add_xaxis(xaxis_data=x)
        .add_yaxis(series_name=time[i], y_axis=ys[i])
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
    )
)
bar.render()
