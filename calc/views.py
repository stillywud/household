#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.shortcuts import render_to_response, get_object_or_404
from .utils import list_items, del_item, gen_serial_no
from .models import *
from .forms import *
import json
from django.db import transaction
import logging
logger = logging.getLogger('django.request')


def login(request, template_name):
    return auth_login(request, template_name)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


@login_required
@csrf_exempt
def password_change(request, template_name):
    if request.method == "GET":
        form = PasswordForm()
        return render_to_response(template_name, locals())
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password']
            if not user.check_password(password):
                info = "原密码错误！"
                return render_to_response(template_name, locals())
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                info = "两次输入密码不一致！"
                return render_to_response(template_name, locals())
            user.set_password(password1)
            user.save()
            info = "密码修改成功！"
        else:
            errors = form.errors
        return render_to_response(template_name, locals())


@login_required
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('calc.views.spend_list'))
    return HttpResponseRedirect("/accounts/login/")


@login_required
@csrf_exempt
def spend_list(request, template_name):
    spends = Spending.objects.all()
    if request.method == "GET":
        form = SpendQueryForm()
        spends = spends.filter(status=0)
    elif request.method == "POST":
        form = SpendQueryForm(request.POST)
        payer = request.POST.get('payer')
        status = request.POST.get('status')
        calc_id = request.POST.get('calcId')
        if payer:
            spends = spends.filter(payer__id=payer)
        if status:
            spends = spends.filter(status=status)
        if calc_id:
            spends = spends.filter(calcId=calc_id)
    page, page_size = list_items(request, spends)
    return render_to_response(template_name, locals())


@login_required
@csrf_exempt
def spend_add(request, template_name):
    if request.method == "GET":
        form = SpendForm()
    elif request.method == "POST":
        form = SpendForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calc.views.spend_list'))
        else:
            errors = form.errors
    return render_to_response(template_name, locals())


@login_required
def spend_delete(request, pk):
    return del_item(Spending, pk)


@login_required
@csrf_exempt
@transaction.commit_manually
def spend_calc(request):
    if request.method == "POST":
        try:
            spend_ids = request.REQUEST.getlist('spend_id')
            spends = Spending.objects.filter(id__in=spend_ids)
            total_mount = 0
            serial_no = gen_serial_no()
            #累计成员消费金额
            expense_dict = {}
            #累计成员付款金额
            pay_dict = {}
            #累计结算结果金额
            amount_dict = {}
            for spend in spends:
                amount = spend.amount
                payer = spend.payer
                #累计付款人的支付金额
                pay_money = pay_dict.get(payer, 0)
                pay_money += amount
                pay_dict[payer] = pay_money

                #累计支付总额
                total_mount += amount
                #计算成员的平均消费
                members = spend.members.all()
                size = len(members)
                ave_money = round(amount / size, 2)
                #累计成员的消费金额
                for m in members:
                    m_exp = expense_dict.get(m, 0)
                    m_exp += ave_money
                    expense_dict[m] = m_exp
                    #计算消费金额
                    u_exp_money = amount_dict.get(m, 0)
                    u_exp_money += ave_money
                    amount_dict[m] = u_exp_money
                    #m.bill_user.add()
                amount_dict[payer] = amount_dict.get(payer, 0) - amount
                spend.status = 1
                spend.calcId = serial_no
                spend.save()
            calculate = Calculate(
                id=serial_no,
                totalAmount=total_mount,
                user=request.user
            )
            calculate.save()
            for u, exp in expense_dict.items():
                bill = Bill(
                    calc=calculate,
                    user=u,
                    amount=amount_dict.get(u, 0),
                    expense=exp,
                    pay=pay_dict.get(u, 0)
                )
                bill.save()
        except Exception, e:
            transaction.rollback()
            logger.error(e, exc_info=e)
            resp = json.dumps({"state": 0, "msg": "系统异常，结算失败"})
            return HttpResponse(resp, content_type="application/json")
        else:
            transaction.commit()
            # resp = json.dumps({"state": 1, "msg": "成功"})
    return HttpResponseRedirect(reverse('calc.views.bill_details', args=(serial_no,)))


@login_required
def calc_list(request, template_name):
    page, page_size = list_items(request, Calculate.objects.all())
    return render_to_response(template_name, locals())


@login_required
def bill_list(request, template_name):
    page, page_size = list_items(request, Bill.objects.all())
    return render_to_response(template_name, locals())


@login_required
def bill_details(request, pk, template_name):
    calculate = Calculate.objects.filter(id=pk)[0]
    bills = Bill.objects.filter(calc__id=pk)
    page, page_size = list_items(request, Spending.objects.filter(calcId=pk))
    return render_to_response(template_name, locals())
