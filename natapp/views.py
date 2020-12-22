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
    error_msg = ''
    if request.method == "GET":
        IDC_list = models.IDC_IP_LIST.objects.all()
        idc = request.GET.get('idc')
        IDCS = models.IDC_IP_LIST.objects.filter(IDC=idc)

        ipPool_data_in = []
        for i in IDCS:
            IDC = i.IDC
            IP_list = list(eval(i.POOL1))

            for ip in IP_list:
                flow_data = es.Flow_traffic_in(IDC, ts15, ts, ip)
                ipPool_data_in.append(flow_data)

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
        ipPool_data_out = []
        for i in IDCS:
            IDC = i.IDC
            IP_list = list(eval(i.POOL1))

            for ip in IP_list:
                flow_data = es.Flow_traffic_out(IDC, ts15, ts, ip)
                ipPool_data_out.append(flow_data)

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
                "data": [x["transfer_in"] for x in di[k]]
            }
            series_out.append(ob)


        return render(request, 'flow.html', {'idc_list': IDC_list, 'legend': legend, 'yaxis': yaxis, 'series': series, 'legend_out': legend_out, 'yaxis_out': yaxis_out, 'series_out': series_out})

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

        IDCS = models.IDC_IP_LIST.objects.filter(IDC=idc)
        IDCS_list = models.IDC_IP_LIST.objects.all()

        for i in IDCS:
            IDC = i.IDC
            IP_list = list(eval(i.POOL1))

        # dtime = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y.%m.%d %H:%M")
        dtime = (datetime.datetime.now().strftime("%Y.%m.%d %H:%M"))
        dtime_15ago = (datetime.datetime.now() + datetime.timedelta(minutes=-15)).strftime("%Y.%m.%d %H:%M")

        ts = int(time.mktime(time.strptime(dtime, "%Y.%m.%d %H:%M")))
        ts15 = int(time.mktime(time.strptime(dtime_15ago, "%Y.%m.%d %H:%M")))

        xlist = ['111.206.250.195', '111.206.250.201', '111.206.250.227', '111.206.250.233']
        es = es_model.EsHandler()
        all_data = []
        for ip in xlist:
            flow_data = es.Flow_traffic_in('bjcc', ts15, ts, ip)
            all_data.append(flow_data)

        di = dict()
        for f_data in all_data:
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



        return render(request, 'test2.html', {'idc_list': IDCS, 'all_data':IDCS_list, 'ips_list': IP_list, 'flow_data': all_data, 'legend': legend, 'yaxis': yaxis, 'series': series})
        # return render(request, 'test2.html', {'idc_list': IDC})
        # return render(request, 'test2.html')








def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="bar-基本示例", subtitle="我是副标题"))
            .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bar_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/test.html").read())
