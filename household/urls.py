#coding:utf-8
from django.conf.urls import patterns, include, url
from calc.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'household.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^password/change/$', password_change, {'template_name': 'password.html'}),

    url(r'^$', index),
    url(r'^spend/list/$', spend_list, {'template_name': 'spend/spend_list.html'}),
    url(r'^spend/add/$', spend_add, {'template_name': 'spend/spend_form.html'}),
    url(r'^spend/delete/(?P<pk>\d+)/$', spend_delete),
    url(r'^spend/calc/$', spend_calc),
    url(r'^calc/list/$', calc_list, {'template_name': 'calc/calc_list.html'}),
    url(r'^bill/list/$', bill_list, {'template_name': 'bill/bill_list.html'}),
    url(r'^bill/details/(?P<pk>\w+)/$', bill_details, {'template_name': 'bill/bill_details.html'}),

)




