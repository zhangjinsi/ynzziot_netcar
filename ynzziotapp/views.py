#coding=utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect

import time
import json
from ynzziotapp import models
from ynzziotapp.forms import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from logger import logger
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,InvalidPage,EmptyPage, PageNotAnInteger
from django.conf import settings
from response import Response

# Create your views here.


@login_required
def index(request):


    return render(request, 'index.html', locals())

@login_required
def positionget(request):
    obj = models.Deviceinforeal.objects.all().values('device_number','serial_number','order_number','time','longitude','latitude','speed','management_status')
    data = list(obj)

    for item in data:
        serial_number=item['serial_number']
        carinfoobj = models.Carinfo.objects.get(bounddevice=serial_number)
        item['device_number'] = carinfoobj.license_plate
        timeArray = time.localtime(item['time'])
        item['time'] = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)

    data = json.dumps(data)


    return HttpResponse(data)

@login_required
def position(request):
    driver_count = models.Driver.objects.all().count()
    car_count = models.Deviceinforeal.objects.all().count()
    company_count = models.Netcarcompany.objects.all().count()
    return render_to_response('map/position.html',{'car_count':car_count,'driver_count':driver_count,'company_count':company_count})

@login_required
def trackback(request):
    license_plate = request.POST.get("license_plate")
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")


    if startTime and endTime:
        starttime = time.mktime(time.strptime(startTime,"%Y-%m-%d %H:%M:%S"))

        endtime = time.mktime(time.strptime(endTime,"%Y-%m-%d %H:%M:%S"))



        #work_List = models.Deviceinfohis.objects.filter(Q(car_info__license_plate=license_plate)&Q(time__gte=starttime)&Q(time__gte=endtime)).values('car_info__license_plate','time','longitude','latitude')
        serialnumber = models.Carinfo.objects.get(license_plate=license_plate).bounddevice

        work_List = models.Deviceinfohis.objects.filter(serial_number=serialnumber,time__gte=starttime,time__lte=endtime).values('device_number','serial_number','time','longitude','latitude').order_by('time')

        work_List = list(work_List)
        for item in work_List:
            item['device_number'] = license_plate

        work_List = json.dumps(work_List)

        print license_plate,startTime,endTime,work_List

        return HttpResponse(work_List)
    return render_to_response('map/track_playback.html')

@login_required
def divisionnumber(request):
    wuhua_count = models.Deviceinforeal.objects.filter(division_number=530102).count()
    xishan_count = models.Deviceinforeal.objects.filter(division_number=530112).count()
    panlong_count = models.Deviceinforeal.objects.filter(division_number=530103).count()
    guandu_count = models.Deviceinforeal.objects.filter(division_number=530111).count()
    chenggong_count = models.Deviceinforeal.objects.filter(division_number=530114).count()

    division_number = [wuhua_count, xishan_count, panlong_count, guandu_count, chenggong_count]
    return HttpResponse(division_number)

def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect('/')
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

# 注销
@login_required
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect('/login/')

# 注册
@login_required
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


#分页代码
def getPage(request,driverlist):
    paginator = Paginator(driverlist,10)
    try:
        page = int(request.GET.get('page',1))
        driverlist = paginator.page(page)
    except (EmptyPage, InvalidPage,PageNotAnInteger):
        driverlist = paginator.page(1)
    return driverlist

#驾驶员信息查询
@login_required
def select_driver(request):

    owned_company = request.POST.get("owned_company",'')
    name = request.POST.get("name",'')
    license_number = request.POST.get("license_number",'')
    certificationauthority = request.POST.get("certificationauthority",'')
    data = owned_company+name+license_number+certificationauthority

    if data:
        driverlist = models.Driver.objects.filter(owned_company__icontains=owned_company,name__icontains=name,license_number__icontains=license_number,certificationauthority__icontains=certificationauthority)

        driverlist = getPage(request,driverlist)

    else:
        driverlist = models.Driver.objects.all()
        driverlist = getPage(request,driverlist)

    return render(request, 'driver/driver.html',locals())

@login_required
def driver_more_info(request):
    id = request.GET.get('id', None)
    driverlist = models.Driver.objects.get(id=id)
    photo = settings.MEDIA_URL+str(driverlist.avatar)

    return render(request, 'driver/moreinfo_driver.html', locals())

#车辆信息查询
@login_required
def select_car(request):

    license_plate = request.POST.get("license_plate",'')
    car_owner = request.POST.get("car_owner",'')
    fueltype = request.POST.get("fueltype",'')
    bounddevice = request.POST.get("bounddevice",'')
    data = license_plate+car_owner+fueltype+bounddevice

    if data:
        carlist = models.Carinfo.objects.filter(license_plate__icontains=license_plate,car_owner__icontains=car_owner,fueltype__icontains=fueltype,bounddevice__icontains=bounddevice)
        carlist = getPage(request,carlist)

    else:
        carlist = models.Carinfo.objects.all()
        carlist = getPage(request,carlist)

    return render(request, 'car/car.html',locals())

@login_required
def car_more_info(request):
    id = request.GET.get('id', None)
    carlist = models.Carinfo.objects.get(id=id)

    return render(request, 'car/moreinfo_car.html', locals())

#公司信息查询
@login_required
def select_company(request):

    companyname = request.POST.get("companyname",'')
    uniformsocialcreditcode = request.POST.get("uniformsocialcreditcode",'')
    registrydivisions = request.POST.get("registrydivisions",'')
    economicoperationtype = request.POST.get("economicoperationtype",'')
    data = companyname+uniformsocialcreditcode+registrydivisions+economicoperationtype

    if data:
        companylist = models.Netcarcompany.objects.filter(companyname__icontains=companyname,uniformsocialcreditcode__icontains=uniformsocialcreditcode,registrydivisions__icontains=registrydivisions,economicoperationtype__icontains=economicoperationtype)
        companylist = getPage(request,companylist)

    else:
        companylist = models.Netcarcompany.objects.all()
        companylist = getPage(request,companylist)

    return render(request, 'company/company.html',locals())

@login_required
def company_more_info(request):
    id = request.GET.get('id', None)
    companylist = models.Netcarcompany.objects.get(id=id)

    return render(request, 'company/moreinfo_company.html', locals())

#数据分析
from datamodel import DataModel
import formatdata
@login_required
def analysishtml(request):
    return render(request, 'analysis.html', locals())

@login_required
def analysis(request):

    dims = request.GET.get('dims',None)

    if not dims:
        json_data = Response.responseJson(Response.INPUT_EMPTY,'输入指标为空')
        json_data = json.dumps(json_data)
        return HttpResponse(json_data)
        #获取数据

    sdate=request.GET.get('sdate','')
    edate=request.GET.get('edate','')
    params = {
        'sdate' : sdate,
        'edate' : edate
    }

    data = DataModel().get_data(dims=dims,args=params)


    #格式化数据
    dims = {
        'name' : dims,
        'type' : 'bar',
        'data' : data
    }

    res_data = formatdata.format_data(dims=dims)


    res_data['title'] = '车辆每天注册数量关系图'

    json_data = Response.responseJson(Response.SUCCESS,data=res_data,msg='获取数据成功')
    json_data = json.dumps(json_data)


    #返回数据
    return HttpResponse(json_data)