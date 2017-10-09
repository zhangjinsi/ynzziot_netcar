#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'
from collections import defaultdict

def format_data(dims=None):
    '''
    格式化数据
    :param dims:
    :return:
    输出数据option = {

         'xAxis': ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],
         'series': [{
             'name': '销量',
             'data': [5, 20, 36, 10, 10, 20]
         }]
    }

    '''
    data = dims.get('data',[])
    name = dims.get('name','')
    type = dims.get('type','bar')

    dict_data = defaultdict(list)


    for item in data: #{'2017-09-16':[144, 56]}
        key = item.get('record_date',None)
        dict_data[key].append(item.get(name))

    axis_x = []
    axis_y = []
    temp = sorted(dict_data.items(),key=lambda x:x[0],reverse=False)
    for key, obj in temp:
        axis_x.append(key) #fdate
        sum_data = sum([num for num in obj if isinstance(num, (float,int,long))])
        axis_y.append(sum_data)

    dims = {
        'xAxis' : axis_x,
        'series' : [{
            'name' : name,
            'data' : axis_y,
            'type' : type
        }]
    }
        #print dims
    return dims