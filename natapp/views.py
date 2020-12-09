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
        IDC = models.IDC_IP_LIST.objects.all()
        return render(request, 'index.html', {'idc_list': IDC})

    elif request.method == "POST":
        IDC = models.IDC_IP_LIST.objects.filter(IDC="bjcc")
        return render(request, 'index.html', {'idc_list': IDC})
    return render(request, 'index.html')


def Idc_graph(request):
    error_msg = ''
    if request.method == "GET":
        idc = request.GET.get('idc')
        IDC = models.IDC_IP_LIST.objects.filter(IDC=idc)
        for i in IDC:
            IDC = i.IDC
            IP_list = list(eval(i.POOL1))

        # flow_data = es_model.EsHandler.get_flow_data('bjcc', 1607505780, '111.206.250.195')

        return render(request, 'flow.html', {'idc_list': IDC, 'ips_list': IP_list})
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

        for i in IDCS:
            IDC = i.IDC
            IP_list = list(eval(i.POOL1))
        flow_data = es_model.EsHandler.get_flow_data('bjcc', 1607505780, '111.206.250.195')
        return render(request, 'test2.html', {'idc_list': IDC, 'ips_list': IP_list, 'flow_data': flow_data})
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
