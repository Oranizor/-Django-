from django.http import JsonResponse
import json

def dispatcher(request):
    # 如果是GET属性 则把参数给到request.params
    if request.method=='GET':
        request.params=request.GET

    # 如果是POST/PUT/DELETE属性 则从request对象的body中取出数据给到request.params
    elif request.method in ['POST','PUT','DELETE']:
        #.load把json字符串变成json对象
        request.params=json.loads(request.body)

    action=request.params['action']
    if action == 'list_customer':
        return listCustomers(request)
    elif action=='add_customer':
        return addCustomer(request)
    elif action=='modify_customer':
        return modifyCustomers(request)
    elif action=='delete_customer':
        return deleteCustomer(request)
    else:
        return JsonResponse({'ret':1,'msg':'不支持该类型的http请求'})
