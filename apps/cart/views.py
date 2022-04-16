from django.shortcuts import render
from django_redis import get_redis_connection
from utils.list_mod_ult import img_url
from ..commodity.models import CommoditySKU
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from utils.commodity_change import commdity_change
import json

def cart(request):
    context = {}
    conn = get_redis_connection('default')
    cart_id = 'cart_%d' % request.session['info']['id']

    # 商品总数
    com_all_num = conn.hlen(cart_id)
    context['com_all_num'] = com_all_num

    com_all = []
    com_all_id = conn.hgetall(cart_id)
    Count = 0

    if com_all_id:
        for i, j in com_all_id.items():
            temp = CommoditySKU.objects.filter(id=i)
            img = img_url(temp)[0]
            com_all.append([temp.first(), img, [int(j), int(j) * temp.first().price]])
            Count += int(j) * temp.first().price
        context['com_all'] = com_all
        context['count'] = Count

    return render(request, '../templates/cart.html', context)


@csrf_exempt
def cart_change(request):
    res = commdity_change(request,2)
    return HttpResponse(res)

@csrf_exempt
def cart_del(request):
    com_id = request.POST['com_id']
    cart_key = 'cart_%d' % request.session['info']['id']
    # 链接redis
    conn = get_redis_connection('default')
    if request.session['info']['id']:
        if conn.hdel(cart_key, com_id) == 1:
            return HttpResponse(json.dumps({'status':True}, ensure_ascii=False))
    return HttpResponse(json.dumps({'status':False}, ensure_ascii=False))