import requests
import json
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType


"""class province:
    def __init__(self,area,confirmed,suspect,healed,dead):
        self.area = area
        self.confirmed = confirmed
        self.suspect = suspect
        self.healed = healed
        self.dead = dead
        """

#定义访问网页的函数
def get_url(url,headers):
    r = requests.get(url,headers = headers)
    return r

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}

data = get_url(url,headers).json()['data']  #把得到的数据用json打开并得到里边的data
data = json.loads(data)  #将json格式转化成py格式的data
time = data["lastUpdateTime"]
data = data["areaTree"][0]["children"]

total = []
'''for each in data:
    prov = province(each['name'],each['total']['confirm'],each['total']['suspect'],each['total']['dead'],each['total']['heal'])
    total.append(prov)
print((total))'''

area = list()
confirmed = []
suspect = []
dead = []
healed=[]
for each in data:
    '''total.append(dict(地区 = each['name'],确诊人数 = each['total']['confirm'],疑似人数 = each['total']['suspect'],死亡人数 = each['total']['dead'],治愈人数 = each['total']['heal']))
print(total)'''
    confirmed.append([each['name']+'确诊',each['total']['confirm']])
    suspect.append([each['name']+"疑似",each['total']['suspect']])
    dead.append([each['name']+"死亡",each['total']['dead']])
    healed.append([each['name']+'治愈',each['total']['heal']])

    '''

    area.append(["地区：",each['name']])
    confirmed.append(["确诊人数：",each['total']['confirm']])
    suspect.append(['疑似人数',each['total']['suspect']])
    dead.append(['死亡人数',each['total']['dead']])
    healed.append(['治愈人数',each['total']['heal']])  '''

def base_info():
    geo = Geo()
    geo.width = "1440px"
    geo.height = "680px"
    geo.add_schema(maptype="china")
    geo.add("确诊人数",confirmed,type_ = ChartType.EFFECT_SCATTER)
    geo.add("疑似人数",suspect,type_ = ChartType.EFFECT_SCATTER)
    geo.add("死亡人数",dead,type_ = ChartType.EFFECT_SCATTER)
    geo.add("治愈人数",healed,type_ = ChartType.EFFECT_SCATTER)
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False,background_color = '#61a0a8'))
    geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(),title_opts=opts.TitleOpts(title="中国ncov-2019疫情动态\n上一次数据更新时间：\n"+time))
    
    return geo
c = base_info()
c.render(path = r'ncov-2019.html')






