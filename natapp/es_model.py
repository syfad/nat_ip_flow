#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020
# @Author  : SunYunfeng(sun_admin@126.com)
# @Disc    : 
# @Disc    : support python 2.x and 3.x

from elasticsearch import Elasticsearch as Elast
from elasticsearch import Elasticsearch
from django.conf import settings
import time, datetime




class EsHandler(object):
    def __init__(self, host=settings.ES[0], port=int(settings.ES[1]), es_user=settings.ES_USER,
                 es_password=settings.ES_PASSWORD):
        self.host = host
        self.port = port
        if es_user:
            self.es = Elast(host=self.host, port=self.port, timeout=6000, http_auth=(es_user, es_password))

        else:
            self.es = Elast(host=self.host, port=self.port, timeout=6000)
        dtime = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y.%m.%d")
        self.index_prefix = ("net_ports_" + dtime)

    def Get_res(self, index, body):
        res = self.es.search(index=index, body=body)
        return res

    def ConvertMB(self, Bytes):
        if type(Bytes) == int:
            convert = ("%.2f" % (Bytes / 1000 / 1000))
            return convert
        else:
            return ''

    def ConvertStime(self, stime):
        try:
            d = time.localtime(stime)
            time_str = time.strftime('%Y-%m-%d %H:%M', d)
            # 2015-08-28 16:43
            return time_str
        except Exception as e:
            print(e)
            return ''

    def flow_data(self, idc, mtime_ago, nowtime, ip):
        # global res_flow
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "IDC": idc
                            }
                        },
                        {
                            "range": {
                                "TIMESTAMP": {"gte": mtime_ago, "lte": nowtime}
                            }
                        },
                        {
                            "term": {
                                "IP": ip
                            }
                        }
                    ]
                }
            },
        }
        try:
            flow_data = []
            result = self.Get_res(self.index_prefix, body)

            for i in result['hits']['hits']:
                flowBytes_in = i['_source']['FLOW_Total_IN']
                flowBytes_out = i['_source']['FLOW_Total_OUT']
                time_s = i['_source']['TIMESTAMP']
                IP = i['_source']['IP']
                #格式化数据
                v_Transfer_in = self.ConvertMB(flowBytes_in)
                v_Transfer_out = self.ConvertMB(flowBytes_out)
                time_s = self.ConvertStime(time_s).split(' ')[1]

                data_flow = {"time_s": time_s, "IP": IP, "transfer_in": v_Transfer_in, "transfer_out": v_Transfer_out}
                flow_data.append(data_flow)
            flow_data.sort(key=lambda e: e.__getitem__('time_s'))
            return flow_data
        except Exception as e:
            print(e)


