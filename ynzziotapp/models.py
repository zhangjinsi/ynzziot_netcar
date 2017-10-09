#coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True, null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username



class Carinfo(models.Model):
    license_plate = models.CharField(max_length=64, verbose_name='车牌号码')
    car_owner = models.CharField(max_length=64, verbose_name='车主')
    registration_location = models.CharField(max_length=32, verbose_name='车辆注册地点')
    vehicle_type = models.CharField(max_length=32, verbose_name='车辆类型')
    body_color = models.CharField(max_length=32, verbose_name='车身颜色')
    weight = models.IntegerField(verbose_name='核定重量')
    date_of_inspection = models.BigIntegerField(verbose_name='年审日期')
    record_date = models.BigIntegerField(verbose_name='登记日期')
    busload = models.IntegerField(verbose_name='核定载客位')
    labelnumber = models.CharField(max_length=64, verbose_name='车辆厂牌')
    transportcertificate = models.CharField(max_length=64, verbose_name='运输证字号')
    tcissuingauthority = models.CharField(max_length=64, verbose_name='运输证发证机构')
    enginenumber = models.CharField(max_length=64, verbose_name='发动机号')
    vinnumber = models.CharField(max_length=64, verbose_name='车辆VIN码')
    fueltype = models.CharField(max_length=64, verbose_name='车辆燃料类型')
    displacement = models.FloatField(verbose_name='发动机排量')
    insurancecompany = models.CharField(max_length=64, verbose_name='保险公司')
    insurancenumber = models.CharField(max_length=64, verbose_name='保险号')
    insurancetype = models.CharField(max_length=64, verbose_name='保险类型')
    insuranceamount = models.FloatField(max_length=64, verbose_name='保险金额')
    insuranceeffectivedate = models.BigIntegerField(verbose_name='保险生效日期')
    insuranceexpirationdate = models.BigIntegerField(verbose_name='保险到期日期')
    totalmileage = models.IntegerField(verbose_name='行驶总里程')
    bounddevice = models.CharField(max_length=64, verbose_name='绑定的设备')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    class Meta:
        verbose_name = '车辆信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.license_plate


class Deviceinfohis(models.Model):
    device_number = models.CharField(max_length=64, verbose_name='设备编号')
    serial_number = models.CharField(max_length=64, verbose_name='设备序列号')
    order_number = models.CharField(max_length=64, verbose_name='订单编号')
    division_number = models.CharField(max_length=64, verbose_name='行政区划编号')
    time = models.BigIntegerField(verbose_name='定位时间')
    longitude = models.CharField(max_length=64, verbose_name='经度')
    latitude = models.CharField(max_length=64, verbose_name='纬度')
    speed = models.FloatField(verbose_name='瞬时速度')
    altitude = models.FloatField(verbose_name='海拔高度')
    direction_angle = models.CharField(max_length=64, verbose_name='方向角')
    management_status = models.CharField(max_length=32, verbose_name='经营状态')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')
    class Meta:
        verbose_name = '设备工作历史信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.serial_number


class Deviceinforeal(models.Model):
    device_number = models.CharField(max_length=64, verbose_name='设备编号')
    serial_number = models.CharField(max_length=64, verbose_name='设备序列号')
    order_number = models.CharField(max_length=64, verbose_name='订单编号')
    division_number = models.CharField(max_length=64, verbose_name='行政区划编号')
    time = models.BigIntegerField(verbose_name='定位时间')
    longitude = models.CharField(max_length=64, verbose_name='经度')
    latitude = models.CharField(max_length=64, verbose_name='纬度')
    speed = models.FloatField(verbose_name='瞬时速度')
    altitude = models.FloatField(verbose_name='海拔高度')
    direction_angle = models.CharField(max_length=64, verbose_name='方向角')
    management_status = models.CharField(max_length=32, verbose_name='经营状态')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')
    class Meta:
        verbose_name = '设备工作实时信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.serial_number


class Driver(models.Model):
    avatar = models.ImageField(upload_to='driver/%Y/%m', default='driver/default.png', max_length=200, blank=True, null=True, verbose_name='驾驶员头像')
    owned_company = models.CharField(max_length=64, verbose_name='所属公司')
    identifier = models.CharField(max_length=64, verbose_name='司机编号')
    name = models.CharField(max_length=64, verbose_name='驾驶员姓名')
    license_number = models.CharField(max_length=24, verbose_name='驾驶证号')
    gender = models.NullBooleanField(verbose_name='性别')
    nationality = models.CharField(max_length=32, verbose_name='国籍')
    birth = models.BigIntegerField(verbose_name='出生日期')
    quasi_car_type = models.CharField(max_length=8, verbose_name='准驾车型')
    issue_date = models.BigIntegerField(verbose_name='初次领证日期')
    valid_date = models.BigIntegerField(verbose_name='有效日期')
    phone_number = models.CharField(max_length=64, verbose_name='电话号码')
    nation = models.CharField(max_length=32, verbose_name='驾驶员民族')
    maritalstatus = models.NullBooleanField(verbose_name='驾驶员婚姻状况')
    car_info = models.CharField(max_length=64, verbose_name='所驾驶车牌号码')
    driverdegree = models.CharField(max_length=32, verbose_name='驾驶员学历')
    cruisedrivers = models.NullBooleanField(verbose_name='是否巡游出租驾驶员')
    certificationauthority = models.CharField(max_length=64, verbose_name='发证机构')
    qualificatcertificatdate = models.BigIntegerField(verbose_name='资格发证日期')
    qualificatvaliditydate = models.BigIntegerField(verbose_name='资格有效期止')
    trainingcoursename = models.CharField(max_length=64, verbose_name='培训课程名称')
    trainingstarttime = models.BigIntegerField(verbose_name='培训开始时间')
    trainingendtime = models.BigIntegerField(verbose_name='培训结束始时间')
    lengthoftraining = models.FloatField(verbose_name='培训时长')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    class Meta:
        verbose_name = '驾驶员信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.license_number

class Netcarcompany(models.Model):
    companyname = models.CharField(max_length=64, verbose_name='公司名称')
    uniformsocialcreditcode = models.CharField(max_length=64, verbose_name='统一社会信用代码')
    registrydivisions = models.CharField(max_length=64, verbose_name='注册地行政区划')
    economicoperationtype = models.CharField(max_length=64, verbose_name='经营业户经济类型')
    registeredcapital = models.IntegerField(verbose_name='注册资本')
    legalrepresentative = models.CharField(max_length=64, verbose_name='法人代表')
    legalpersonidentification = models.CharField(max_length=24, verbose_name='法人身份证号')
    phone_number = models.CharField(max_length=64, verbose_name='电话号码')
    address = models.CharField(max_length=64, verbose_name='通讯地址')
    businessscope = models.CharField(max_length=256, verbose_name='经营范围')
    managementarea = models.CharField(max_length=64, verbose_name='经营区域')
    businessname = models.CharField(max_length=64, verbose_name='业户名称')
    certificationauthority = models.CharField(max_length=64, verbose_name='发证机构')
    issuedate = models.BigIntegerField(verbose_name='发证日期')
    validitydate = models.BigIntegerField(verbose_name='有效期止')
    licensestatus = models.CharField(max_length=32, verbose_name='证照状态')
    platformcarnumber = models.BigIntegerField(verbose_name='平台注册网约车辆数')
    platformdrivernumber = models.BigIntegerField(verbose_name='平台注册驾驶员数')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')


    class Meta:
        verbose_name = '网约车平台信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.companyname

class Imagedevice(models.Model):
    device_number = models.CharField(max_length=64, verbose_name='设备编号')
    serial_number = models.CharField(max_length=64, verbose_name='设备序列号')
    order_number = models.CharField(max_length=64, verbose_name='订单编号')
    carimage = models.ImageField(upload_to='imagedevice/%Y/%m', default='imagedevice/default.png', max_length=200, blank=True, null=True, verbose_name='车内照片')
    time = models.BigIntegerField(verbose_name='拍照时间')
    updatedate = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    class Meta:
        verbose_name = '车内拍照信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.carimage









