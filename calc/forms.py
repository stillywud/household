#coding:utf-8

from django import forms
from .models import *


class SpendForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpendForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Spending
        exclude = ('calcId',)


class SpendQueryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpendQueryForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Spending
        fields = ('payer', 'status', 'calcId')


class PasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs.update({'class': 'form-control'})

    password = forms.CharField(label="原密码", required=True)
    password1 = forms.CharField(label="新密码", required=True)
    password2 = forms.CharField(label="确认密码", required=True)