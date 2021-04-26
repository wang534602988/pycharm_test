from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Pie, Grid
import pandas as pd


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
    num_list_new = map(lambda x: str(x), y)
    y = list(num_list_new)
    ys.append(y)
    time.append(df.iloc[i][0])
tl = Timeline()
for i in range(0, len(time)):
    data_pair = [list(z) for z in zip(x, ys[i])]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name=time[i], y_axis=ys[i])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
        )
    )
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(x, ys[i])],
            radius=[60, 0],
            center=["70%", "20%"],
            label_opts=opts.LabelOpts(is_show=False)
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="80%", orient="vertical"
            ),
        )

    )
    grid = (
        Grid(init_opts=opts.InitOpts(width="1800px", height="800px"))
            .add(bar, grid_opts=opts.GridOpts(pos_left="5%", width=500, height=200))
            .add(pie, grid_opts=opts.GridOpts(pos_right="0%", pos_top='80%', width=200, height=250))
    )
    tl.add(grid, time[i])
tl.add_schema(
    pos_top="87%",
    pos_left='0%',
    label_opts=opts.LabelOpts(rotate=30,position='insideBottom')
)
tl.render("tab.html")
