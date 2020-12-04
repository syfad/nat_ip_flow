from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from natapp import models


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
            #res.set_cookie('username_cookie', user, max_age=600)
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
    return render(request,'index.html')

def Idc_graph(request):
    error_msg = ''
    if request.method == "GET":
        IDC = models.IDC_IP_LIST.objects.all()
        return render(request, 'flow.html', {'idc_list': IDC})

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