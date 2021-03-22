from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from common.models import Customer

def listorders(request):
    return HttpResponse("下面是系统中的所有订单信息...")


def listcustomers(request):
    # 返回一个QuerySet对象 包含所有的表记录
    # 每条表记录都是一个dict对象
    # key是字段名 value是字段值
    qs=Customer.objects.values()


    #定义返回字符串
    resStr=''
    for customer in qs:
        for name,value in customer.items():
            resStr+=f'{name}:{value}|'
        resStr+='<br>'

    return HttpResponse(qs,resStr)