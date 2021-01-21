from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from natapp import models
import json
from random import randrange
from django.core import serializers
from django.http import HttpResponse
from rest_framework.views import APIView
from pyecharts.charts import Bar
from pyecharts.charts import Kline
from pyecharts import options as opts
from natapp import es_model
import time, datetime
import pymysql



def login(request):
    error_msg = ''
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        # 获取用户通过post提交过来的数据
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        obj = models.Host.objects.filter(username=user, password=pwd).first()

        if obj:

            res = redirect('/monitor/index/')

            # 设置cookie，max_age多少秒之后失效
            res.set_cookie('username_cookie', user, max_age=600)

            return res
        else:
            error_msg = "用户名密码错误"
    return render(request, 'login.html', {'error_msg': error_msg})


def graph(request):
    error_msg = ''
    if request.method == "GET":
        return render(request, 'flow.html')
    elif request.method == "POST":
        # 获取用户通过post提交过来的数据
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        obj = models.IDC_IP_LIST.objects.filter(username=user, passwd=pwd).first()
        if obj:
            res = redirect('admin/')
            # 设置cookie，max_age多少秒之后失效
            # res.set_cookie('username_cookie', user, max_age=600)
            return res
        else:
            error_msg = "用户名密码错误"
            return render(request, 'login.html', {'error_msg': error_msg})


def index(request):
    if request.method == "GET":
        IDC_list = models.IDC_IP_LIST.objects.all()

        return render(request, 'index.html', {'idc_list': IDC_list})

    elif request.method == "POST":
        IDC = models.IDC_IP_LIST.objects.filter(IDC="bjcc")
        return render(request, 'index.html', {'idc_list': IDC})
    # return render(request, 'index.html')


def Idc_graph(request):
    es = es_model.EsHandler()
    dtime = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y.%m.%d %H:%M")
    dtime_15ago = (datetime.datetime.now() + datetime.timedelta(minutes=-15)).strftime("%Y.%m.%d %H:%M")
    ts = int(time.mktime(time.strptime(dtime, "%Y.%m.%d %H:%M")))
    ts15 = int(time.mktime(time.strptime(dtime_15ago, "%Y.%m.%d %H:%M")))

    get_idc = request.GET.get('idc')
    pool_num = request.GET.get('pool_addr')


    error_msg = ''
    if request.method == "GET":
        poll_data = models.IDC_IP_LIST.objects.all()
        Idc_req = models.IDC_IP_LIST.objects.filter(IDC=get_idc)

        #取对应idc机房IP数据
        poll_list = Idc_req.values()

        pool = []
        get_ips = []
        for i in poll_list:
            if i['POOL1'] != '':
                pool.append('POOL1')
            if i['POOL2'] != '':
                pool.append('POOL2')
            if i['POOL3'] != '':
                pool.append('POOL3')
            if i['POOL4'] != '':
                pool.append('POOL4')

            if pool_num == None:
                pool_num = "POOL1"
                get_ips.append(i[pool_num])
            else:
                if i[pool_num] == '':
                    get_ips.append(i['POOL1'])
                else:
                    get_ips.append(i[pool_num])

        # print(get_ips[0])

        #请求in/out,ES接口
        ipPool_data_in = []
        ipPool_data_out = []
        for i in Idc_req:
            IDC = i.IDC
            # IP_list = list(eval(i.POOL1))
            IP_list = list(eval(i.POOL1))

            # for ip in list(eval(get_ips[0])):
            for ip in list(eval(get_ips[0])):
                flow_data = es.Flow_traffic_in(IDC, ts15, ts, ip)
                ipPool_data_in.append(flow_data)

            for ip in list(eval(get_ips[0])):
                flow_data = es.Flow_traffic_out(IDC, ts15, ts, ip)
                ipPool_data_out.append(flow_data)

        #Flow_traffic_in
        di = dict()
        for f_data in ipPool_data_in:
            for i in f_data:
                if i["IP"] in di:
                    di[i["IP"]].append(i)
                else:
                    di[i["IP"]] = [i]

        legend = di.keys()
        yaxis = [x["time_s"] for x in next(iter(di.values()))]

        series = []
        for k in legend:
            ob = {
                "name": k,
                "data": [x["transfer_in"] for x in di[k]]
            }
            series.append(ob)

        #Flow_traffic_out
        di = dict()
        for f_data in ipPool_data_out:
            for i in f_data:
                if i["IP"] in di:
                    di[i["IP"]].append(i)
                else:
                    di[i["IP"]] = [i]

        legend_out = di.keys()
        yaxis_out = [x["time_s"] for x in next(iter(di.values()))]

        series_out = []
        for k in legend:
            ob = {
                "name": k,
                "data": [x["transfer_out"] for x in di[k]]
            }
            series_out.append(ob)


        return render(request, 'flow.html', {'idc_list': poll_data, 'legend': legend, 'yaxis': yaxis, 'series': series, 'legend_out': legend_out, 'yaxis_out': yaxis_out, 'series_out': series_out, 'pool_list': pool, 'get_idc': get_idc})

    elif request.method == "POST":
        # 获取用户通过post提交过来的数据
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        obj = models.IDC_IP_LIST.objects.filter(username=user, passwd=pwd).first()
        if obj:
            res = redirect('admin/')
            # 设置cookie，max_age多少秒之后失效
            # res.set_cookie('username_cookie', user, max_age=600)
            return res
        else:
            error_msg = "用户名密码错误"
            return render(request, 'login.html', {'error_msg': error_msg})






def detail(request):
    if request.method == "GET":
        # idc = request.GET.get('idc')

        IDC = models.IDC_IP_LIST.objects.all()

        return render(request, 'test1.html', {'idc_list': IDC})

def detail1(request):
    if request.method == "GET":
        idc = request.GET.get('idc')
        pool_num = request.GET.get('pool')
        IDCS = models.IDC_IP_LIST.objects.filter(IDC=idc)
        if pool_num == None:
            pool_num = 'POOL1'
        pool_ip_list = models.IDC_IP_LIST.objects.filter(IDC=idc).values(pool_num)
        for pool_list in pool_ip_list:
            pool_list = pool_list['POOL1']

        # dtime = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y.%m.%d %H:%M")
        dtime = (datetime.datetime.now().strftime("%Y.%m.%d %H:%M"))
        dtime_15ago = (datetime.datetime.now() + datetime.timedelta(minutes=-15)).strftime("%Y.%m.%d %H:%M")

        ts = int(time.mktime(time.strptime(dtime, "%Y.%m.%d %H:%M")))
        ts15 = int(time.mktime(time.strptime(dtime_15ago, "%Y.%m.%d %H:%M")))

        # xlist = ['111.206.250.195', '111.206.250.201', '111.206.250.227', '111.206.250.233']
        # xlist = ['111.206.250.196', '111.206.250.202', '111.206.250.228', '111.206.250.234']

        #判断地址池的显示
        IDCS_list = IDCS.values()
        pool=[]

        # ips = IDCS_list[0]
        # if pool_num == None:
        #     pool_num = 'POOL1'
        # pool_ip = ips[pool_num]


        for i in IDCS_list:
            if i['POOL1'] != '':
                pool.append('POOL1')
            if i['POOL2'] != '':
                pool.append('POOL2')
            if i['POOL3'] != '':
                pool.append('POOL3')
            if i['POOL4'] != '':
                pool.append('POOL4')

        es = es_model.EsHandler()
        all_data = []

        for i in IDCS:
            IDC = i.IDC
            # IP_list = list(eval(i.POOL2))

            # 循环获得取得ES接口数据
            for ip in pool_list:
                flow_data = es.Flow_traffic_in(IDC, ts15, ts, ip)
                all_data.append(flow_data)

        di = dict()
        for f_data in all_data:
            for i in f_data:
                if i["IP"] in di:
                    di[i["IP"]].append(i)
                else:
                    di[i["IP"]] = [i]

        # 前端IP的数据
        legend = di.keys()

        # 前端X轴的数
        yaxis = [x["time_s"] for x in next(iter(di.values()))]

        # 前端Y轴的数据
        series = []
        for k in legend:
            ob = {
                "name": k,
                "data": [x["transfer_in"] for x in di[k]]
            }
            series.append(ob)

        return render(request, 'test2.html', {'legend': legend, 'yaxis': yaxis, 'series': series, 'ips': pool_ip, 'pool':pool, 'get_idc': idc, 'pool_ip_list': pool_list})

