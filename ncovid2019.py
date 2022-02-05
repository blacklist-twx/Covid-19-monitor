import requests
import json
from pyecharts.charts import Geo
from pyecharts import options as opts


# 定义访问网页的函数
def get_url(url, headers):
    response = requests.get(url, headers=headers)
    return response


# 数据来源网站
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
# 请求头部
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.116 Safari/537.36'}

response = get_url(url, headers)

data = response.json()['data']  # 把得到的数据转换成json格式并获取data
data = json.loads(data)  # 将json格式转化成json对象
time = data["lastUpdateTime"]
data = data["areaTree"][0]["children"]  # 获取省份细节数据
print(data)

confirmed = []
for each in data:
    confirmed.append((each['name'], str(each['today']['confirm'])))
print(confirmed)


def base_info():
    """地图参数配置"""
    geo = Geo(is_ignore_nonexistent_coord=False)
    geo.width = "1440px"
    geo.height = "680px"
    geo.add_schema(maptype="china") \
        .add(series_name="新增确诊人数", data_pair=confirmed) \
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False, background_color='#61a0a8')) \
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(),
                         title_opts=opts.TitleOpts(title="中国新冠疫情动态\n数据更新时间：\n" + time))
    return geo


map = base_info()
map.render(path=r'ncov-2019.html')
