#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018
# @Author  : SunYunfeng(sun_admin@126.com)
# @Disc    : 
# @Disc    : support python 2.x and 3.x

import os
import sys
from natapp import es_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nat_ip_flow.settings')


flow_data = es_model.EsHandler.get_flow_data('bjcc', 1607505780, '111.206.250.195')

print(flow_data)