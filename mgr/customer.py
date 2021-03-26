from django.http import JsonResponse
from common.models import Customer
import json
from django.http import HttpResponse

def dispatcher(request):
    print(">>>dispatcher检查",request.session)
    # 原来搞了这么久 还没做登陆的验证呢！
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret':302,
            'msg':'未登录',
            'redirect':'/mgr/sign.html',
        },status=302)

    if request.session['usertype']!='mgr':
        return JsonResponse({
            'msg':'用户非mgr类型',
            'redirect':'/mgr/sign.html'
        },status=302)


    # 如果是GET属性 则把参数给到request.params
    print(type(request.body))
    # return HttpResponse("Body:" + str(json.loads(request.body)) + "Method:" + str(request.method))

    if request.method=='GET':
        request.params=request.GET

    # 如果是POST/PUT/DELETE属性 则从request对象的body中取出数据给到request.params
    elif request.method in ['POST','PUT','DELETE']:
        #.load把json字符串变成json对象
        request.params=json.loads(request.body)

    print(request.params)
    action=request.params['action']
    if action == 'list_customer':
        return listCustomers(request)
    elif action=='add_customer':
        return addCustomers(request)
    elif action=='modify_customer':
        return modifyCustomers(request)
    elif action=='delete_customer':
        return deleteCustomers(request)
    else:
        return JsonResponse({'login':1,'data':'不支持该类型的http请求'})

# 处理get的函数（获取）
def listCustomers(request):
    # 获得common.models的Customer的所有数据
    qs = Customer.objects.values()
    # 把qs的格式转化为list
    retlist = list(qs)
    # 补全剩余部分，JsonResponses是用Json格式输出，ret=0代表成功
    return JsonResponse({'ret': 0, 'data': retlist})

def addCustomers(request):
    # request.params里已经包含前端给后端的数据了，data是数据所在的key（人定义的名字啦）
    info = request.params['data']
    record = Customer.objects.create(name=info['name'], phoneNumber=info['phoneNumber'], address=info['address'])
    return JsonResponse({'ret': 0, 'id': record.id})

def modifyCustomers(request):

    customerid=request.params['id']
    newdata=request.params['newdata']

    try:
        customer=Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return {
            'ret':1,
            'msg':f'id为`{customerid}`的客户不存在'
        }

    if'name' in newdata:
        customer.name=newdata['name']
    if 'phoneNumber' in newdata:
        customer.phoneNumber=newdata['phoneNumber']
    if 'address' in newdata:
        customer.address=newdata['address']

    customer.save()

    return JsonResponse({'ret':0})

def deleteCustomers(requset):
    customerid=requset.params['id']

    try:
        customer=Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return {
            'ret':1,
            'msg':f'id为`{customerid}`的客户不存在'
        }

    customer.delete()

    return JsonResponse({'ret': 0})