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

    # object 可以跟:
    # object.all()<注意all输出的是对象>
    # object.value()<如果跟了内容就是输出一列。如果没跟内容就是直接把对象摊开>
    # object.filter()<筛选出一组>
    # object.get()<筛选出一个>
    # object.exclude()<筛选出除了自己的一组>
    # object.exist()<是否存在>
    # object.count()<数个数>
    # object.first()<第一个>
    # object.last()<最后一个>
    # object.aggregate(Max('age'))
    # 各个之间可以链式调用
    #
    # 切片:如果object[1:3] 则只有1号 2号（0号没有 3号没有） 不能是负数
    #
    # 参数 ：属性__运算符（gt lt gte lte in contains endwith...） 前面添加i表示忽略 如iexact
    # pk 表示主键
    #
    # 使用__符 沿表关联方向向下渗透
    # 如grades=Grade.objects.filer(student__s_name='Jack')
    #
    # F对象 输出字段直接的值
    # 当要比较一个类里两个属性的大小 比如 男生比女生多的公司的时候 可以用F函数 F函数输出的是一个数就是字段的值
    # companies=Company.objects.filter(c_boy_num__lt=F('c_girl_num')-15)
    #
    # Q对象 对条件进行封装，以进行逻辑操作
    # companies=Company.object.filter(Q(c_boy_num__gt=1)&Q(c_girl_num__gt=10))
    #
    # 例如：students.objects().filter(name = ‘张三’).values('id'), 只返回名为张三的学生的id,不返回其他属性了。
    # students.objects().all().values('name')即获取到所有的表中的姓名，返回一个字典组成的列表[{‘name’:‘张三’}，{‘name’:‘李四’}，。。。]
    # students.objects().all() 是获取表中所有的数据

    print(">>>>>>all",Customer.objects.all())
    print(">>>>>>value",Customer.objects.all().values())
    print(">>>>>>abc", Customer.abc.all())
    qs=Customer.objects.values()
    # 例如 .../?phoneNumber=139291921

    ph=request.GET.get('phoneNumber',None)

    if ph:
        qs=qs.filter(phoneNumber=ph)

    #定义返回字符串
    resStr=''
    for customer in qs:
        for name,value in customer.items():
            resStr+=f'{name}:{value}|'
        resStr+='<br>'

    return HttpResponse(resStr)