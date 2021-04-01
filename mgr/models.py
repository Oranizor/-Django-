from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserManger(models.Manager):
    def get_queryset(self):
        return super(UserManger,self).get_queryset().filter()
    # super就是父类，会一直找到最父的元素。get_queryset是filter的父类。

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        db_table="www"
        ordering=[]

    # 加了一个方法，不需要迁移
    @classmethod
    def create(cls,p_age=100,p_sex=True):
        return cls()

    user=models.OneToOneField('auth.User',on_delete=models.CASCADE)
    token=models.CharField(max_length=50,verbose_name="认证token")
    #
    # 对象方法
    # -可以调用对象的属性，也可以调用类的属性
    # 类方法
    # -可以调用类属性
    # 静态方法
    # -不能调用


# 监听到post_save事件且发送者是User则执行create_extension_user函数
# 关于@
# 1.作为语法糖 是一个修饰函数 其逻辑是，先不执行被修饰的函数，而是把被修饰的函数作为参数传进修饰函数中，再执行修饰函数。如果修饰函数不执行这个参数（被修饰函数），甚至可能根本不关被修饰函数的事。
# https://www.jb51.net/article/158533.htm
# 2. 使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。
# https://www.runoob.com/python/python-func-classmethod.html
@receiver(post_save, sender=User)
def create_extension_user(sender, instance, created, **kwargs):
    """
    使用信号来触发userprofile 的自定创建和保存
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    print(">>>>6")
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()