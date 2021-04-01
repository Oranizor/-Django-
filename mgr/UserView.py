from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User


class UserView(View):
    def get(self,request,*args,**kwargs):
        users=User.objects.all()
        res_list=[]
        for user in users:
            # 查看对象的所有方法
            print('\n'.join(['%s:%s' % item for item in users.__dict__.items()]))
            res_list.append({
                'username':user.username,
                'password':user.password,
                'auth':user.is_superuser,
            })

        return JsonResponse({
            'code':0,
            'message':'查询成功',
            'content':res_list
        })