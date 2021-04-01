import hashlib

from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.decorators import method_decorator
import json


class TokenRequireView(View):
    """
    获取header 数据
    - request.META.get("header key") 用于获取header的信息
    - 注意的是header key必须增加前缀HTTP，同时大写，例如你的key为username，那么应该写成：request.META.get("HTTP_USERNAME")
    - 另外就是当你的header key中带有中横线，那么自动会被转成下划线，例如my-user的写成： request.META.get("HTTP_MY_USER")
    """
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.filter(userprofile__token=request.META.get('HTTP_TOKEN')).first()
        if not user:
            return JsonResponse({
                'code': 403,
                'message': '认证不通过！'
            })
        return super().dispatch(request, *args, **kwargs)


class UserView(TokenRequireView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        message = []
        for user in users:
            message.append({
                'username': user.username,
                'password': user.password,
                'auth': user.is_superuser,
            })

        return JsonResponse({
            'code': 0,
            'message': message
        })


class LoginView(View):
    print(">>>>1")
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(">>>>2")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({
                'code': 400,
                'message': '用户名或密码错误！'
            })
        else:
            # auth.login(request, user)
            # 生成token
            print(">>>>3")
            token = self.genarate_token(username)
            print(">>>>4")
            user.userprofile.token = token
            print(">>>>5")
            user.save()
            return JsonResponse({
                'code': 0,
                'message': '认证成功!',
                'token': token
            })

    def genarate_token(self, username):
        """
        生成token
        """
        return hashlib.md5(username.encode('utf-8')).hexdigest()

# def signin(request):
#     print(">>>request",request)
#     userName=request.POST.get('username')
#     passWord=request.POST.get('password')
#
#
#     #这里必须TMD写注释了
#     #如果是request.body 得到的直接是data里面数据
#     #如果是request.post 问题可就海了去了
#     #1. 因为axios的method设置为post后 就不会读取后面的?XXX=YYY这样的内容，所以必须靠别的东西模拟(qs)
#     #2. 还要加上协定的名字才能让浏览器知道这个是带了?XXX=YYY这样的内容的(header)
#
#     user=authenticate(username=userName,password=passWord)
#
#     if not user:
#         return JsonResponse({
#             'code':400,
#             'message':'用户名或密码错误'
#         })
#     else:
#         token=genarate_token(userName)
#         print(">>>>现在拿到hash值了")
#         print('\n'.join(['%s:%s' % item for item in user.__dict__.items()]))
#         user.userprofile.token=token
#         print(">>>>更改userprofile")
#         user.save()
#         return JsonResponse({
#             'code':0,
#             'message':'获取token成功',
#             'token':token
#         })
#
# def genarate_token(username):
#     hasha = hashlib.md5(username.encode('utf-8')).hexdigest()
#     print(hasha)
#     return hasha

def signout(request):
    logout(request)
    return JsonResponse({'ret':0})

