from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout

def signin(request):
    userName=request.POST.get('username')
    passWord=request.POST.get('password')


    #这里必须TMD写注释了
    #如果是request.body 得到的直接是data里面数据
    #如果是request.post 问题可就海了去了
    #1. 因为axios的method设置为post后 就不会读取后面的?XXX=YYY这样的内容，所以必须靠别的东西模拟(qs)
    #2. 还要加上协定的名字才能让浏览器知道这个是带了?XXX=YYY这样的内容的(header)

    #print(">>>检查",request.body,request.POST,userName,passWord)
    user=authenticate(username=userName,password=passWord)

    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request,user)
                request.session['usertype']='mgr'
                print(">>>成功登录了")
                return JsonResponse({'ret':0})
            else:
                return JsonResponse({'ret':1,'msg':'请使用管理员账户登录'})
        else:
            return JsonResponse({'ret':1,'msg':'用户已被禁用'})
    else:
        return JsonResponse({'ret':1,'msg':'用户名或密码错误'})


def signout(request):
    logout(request)
    return JsonResponse({'ret':0})