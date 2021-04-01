from django.db import models

#定义数据库表


class CustomerManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)

    address = models.CharField(max_length=200)

    abc=CustomerManger()

