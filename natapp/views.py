from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from natapp import models
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
        obj = models.User.objects.filter(username=user, password=pwd).first()

        if obj:

            res = redirect('/index/')

            # 设置cookie，max_age多少秒之后失效
            # res.set_cookie('username_cookie', user, max_age=600)

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
