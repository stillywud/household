from django.contrib import admin
from .models import *


class SpendingAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payer', 'spendTime', 'status', 'calcId', 'note', 'createTime', 'updateTime')
    list_filter = ('payer', 'spendTime', 'status', 'calcId')
    ordering = ('payer', '-spendTime', 'status', 'calcId', '-createTime', 'updateTime')


class CalculateAdmin(admin.ModelAdmin):
    list_display = ('id', 'totalAmount', 'user', 'createTime')
    list_filter = ('id', 'user')
    ordering = ('id', 'totalAmount', 'user', '-createTime')


class BillAdmin(admin.ModelAdmin):
    list_display = ('calc', 'user', 'amount', 'expense', 'pay', 'createTime')
    list_filter = ('calc', 'user')
    ordering = ('calc', 'user', 'amount', 'expense', 'pay', '-createTime')


admin.site.register(Spending, SpendingAdmin)
admin.site.register(Calculate, CalculateAdmin)
admin.site.register(Bill, BillAdmin)
