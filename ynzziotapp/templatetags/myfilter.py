# -*- coding: utf-8 -*-
from django import template
import time
register = template.Library()


@register.filter
def gender_filter(gender):
    if gender == True:
        result = '男'
    elif gender == False:
        result = '女'
    else:
        result = '未知'

    return result

@register.filter
def long_to_time(time_long):
    time_long = time.localtime(time_long)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_long)
    return time_str

@register.filter
def yes_to_true(input_true):
    if input_true == True:
        result = '是'
    elif input_true == False:
        result = '否'
    else:
        result = '未知'
    return result

# 注册过滤器
# register.filter('month_to_upper', month_to_upper)