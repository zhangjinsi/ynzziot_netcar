import settings
"""ynzziot_netcar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from ynzziotapp import views
from ynzziotapp import upload

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^uploads/(?P<path>.*)$", \
                "django.views.static.serve", \
                {"document_root": settings.MEDIA_ROOT,}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload.upload_image, name='upload_image'),
    url(r'^$', views.index),
    url(r'^positionget/', views.positionget),
    url(r'^position/', views.position),
    url(r'^trackback/', views.trackback),
    url(r'^divisionnumber/', views.divisionnumber),
    url(r'^login/', views.do_login, name='login'),
    url(r'^reg/', views.do_reg, name='reg'),
    url(r'^logout/', views.do_logout, name='logout'),
    url(r'^accounts/login/', views.do_login, name='do_login'),
    url(r'^driverlist/', views.select_driver, name='select_driver'),
    url(r'^driver_more_info/', views.driver_more_info, name='driver_more_info'),
    url(r'^carlist/', views.select_car, name='select_car'),
    url(r'^car_more_info/', views.car_more_info, name='car_more_info'),
    url(r'^companylist/', views.select_company, name='select_company'),
    url(r'^company_more_info/', views.company_more_info, name='company_more_info'),
    url(r'^analysis/', views.analysis, name='analysis'),
    url(r'^analysishtml/', views.analysishtml, name='analysishtml'),
]
