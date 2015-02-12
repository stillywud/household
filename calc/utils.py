#coding:utf-8

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import random
import string
import time


#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
def gen_string(length=20):
    chars = string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])


def gen_serial_no():
    return '%s%06d' % (time.strftime('%Y%m%d%H%M%S'), random.randint(1, 999999))

if __name__ == "__main__":
    print(gen_string(20))
    for i in range(10):
        no = gen_serial_no()
        print('%s, %d' % (no, len(no)))


def list_items(request, items):
    try:
        page_size = int(request.GET.get('page_size', 30))
        if page_size <= 0:
            raise Http404
    except ValueError:
        page_size = 30
    page = request.GET.get('page')
    paginator = Paginator(items, page_size)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items, page_size


def del_item(model, pk):
    try:
        sign_key = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        resp = json.dumps({"state": 0, "msg": "不存在的记录"})
        return HttpResponse(resp, content_type="application/json")
    sign_key.delete()
    resp = json.dumps({"state": 1, "msg": "成功"})
    return HttpResponse(resp, content_type="application/json")
