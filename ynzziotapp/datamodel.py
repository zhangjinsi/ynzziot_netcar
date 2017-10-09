#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from connection.db_mongodb import Connection
from logger import logger
from datetime import datetime
from ynzziotapp import models
from django.db.models.aggregates import Count
import time
import config


class DataModel(object):

    def get_data(self, dims=None, args={}):


        #再从mysql中获取数据

        sdate = args['sdate']

        sdate = time.mktime(time.strptime(sdate,"%Y-%m-%d"))
        edate = args['edate']
        edate = time.mktime(time.strptime(edate,"%Y-%m-%d"))


        #mongo  100000
        #数据库， 集合， 文档
        #时间，访问频率, 定时清除数据
        #bjson
        params = {
            'sql' : str(sdate)+str(edate)
        }
        datenow = datetime.now().date().strftime('%Y-%m-%d')
        db = Connection(host=config.MONGODB_HOST,port=config.MONGODB_PORT,database=config.MONGODB_DB)

        res = db.buniss.find_one(params)

        if not res:
            logger.info('从mysql中查找数据')
            data = models.Carinfo.objects.filter(record_date__gte=sdate,record_date__lte=edate).values('record_date','license_plate').annotate(activeacount=Count('license_plate')).order_by('record_date')#数据量很大的时候就会变得很慢

            for item in data:
                fcount = int(item.get('activeacount', 0))
                item['activeacount'] = fcount
                re_date=item.get('record_date', 0)
                time_long = time.localtime(re_date)
                item['record_date'] = time.strftime("%Y-%m-%d",time_long)


            data = list(data)
            params = {
                'sql' : 'aaa',
                'data' : data,
                'flushdate' : datenow,
                'flushcount' : 1,
            }

            #params={'flushdate': '2017-09-27', 'data': [{'activeacount': 1, 'record_date': '2017-09-07 12:00:00', 'license_plate': u'\u4e91A12345'}, {'activeacount': 1, 'record_date': '2017-09-07 12:00:00', 'license_plate': u'\u4e91A88888'}], 'flushcount': 1, 'sql': '1504195200.01506441600.0'}

            db.buniss.insert_one(params)

        else:
            logger.info('从mongodb中查找数据')
            db.buniss.update(params, {"$set" : {"flushdate": datenow}, "$inc":{"flushcount":1}}, False, True)
            data = res.get('data',[])

        return data

if __name__ == '__main__':
    db = DataModel()

    params = {
            'sdate' : '2017-09-16',
            'edate' : '2017-09-26'
        }
    print db.get_data(dims='chart1',args=params)
