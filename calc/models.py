#coding:utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SPENDING_STATUS_CHOICES = (
    (0, u'开支'),
    (1, u'已结算'),
)


class Spending(models.Model):
    amount = models.FloatField(u'金额')
    payer = models.ForeignKey(User, verbose_name=u'付款人', related_name='payer_user')
    members = models.ManyToManyField(User, verbose_name=u'成员', related_name='members_users')
    spendTime = models.DateTimeField(u'开支时间', default=datetime.now())
    status = models.IntegerField(u'状态', default=0, choices=SPENDING_STATUS_CHOICES)
    calcId = models.CharField(u'结算编号', max_length=50, blank=True)
    note = models.TextField(u'备注')
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(u'修改时间', auto_now=True)

    class Meta:
        db_table = 'household_calc_spending'
        verbose_name = u'开支明细'
        verbose_name_plural = u'开支明细'


class Calculate(models.Model):
    id = models.CharField(u'结算编号', max_length=50, primary_key=True)
    totalAmount = models.FloatField(u'总金额', default=0)
    user = models.ForeignKey(User, verbose_name=u'结算人', related_name='calc_user')
    createTime = models.DateTimeField(u'结算时间', auto_now_add=True)

    class Meta:
        db_table = 'household_calc_calculate'
        verbose_name = u'结算记录'
        verbose_name_plural = u'结算记录'


class Bill(models.Model):
    calc = models.ForeignKey(Calculate, verbose_name=u'结算编号', related_name='bill_calc')
    user = models.ForeignKey(User, verbose_name=u'成员', related_name='bill_user')
    amount = models.FloatField(u'金额', default=0)
    expense = models.FloatField(u'总消费', default=0)
    pay = models.FloatField(u'总付款', default=0)
    createTime = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = 'household_calc_bill'
        unique_together = ('calc', 'user')
        verbose_name = u'账单'
        verbose_name_plural = u'账单'
