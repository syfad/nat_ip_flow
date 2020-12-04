#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018
# @Author  : SunYunfeng(sun_admin@126.com)
# @Disc    : 
# @Disc    : support python 2.x and 3.x

from elasticsearch import Elasticsearch as Elast
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
        # self.date_format = "%Y.%m.%d"
        # self.date_format_m = "%Y"

    def get_res(self, index, body):
        res = self.es.search(index=index, body=body)
        return res

    def get_flow_data(self, IDC, timeStamp, IP):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "IDC": IDC
                            }
                        },
                        {
                            "term": {
                                "TIMESTAMP": timeStamp
                            }
                        },
                        {
                            "term": {
                                "IP": IP
                            }
                        }
                    ]
                }
            },
            "from": "0",
            "size": "1"
        }

        try:
            result = self.get_res(self.index_prefix, body)
            flow_total_in = result['_source']['FLOW_Total_IN']
            flow_total_out = result['_source']['FLOW_Total_OUT']
            res_flow = [flow_total_in, flow_total_out]
        except Exception as e:
            print(e)

        return res_flow
