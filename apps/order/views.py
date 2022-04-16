from django.shortcuts import render
from ..commodity.models import CommoditySKU
from utils.list_mod_ult import img_url
from django_redis import get_redis_connection
from django.http import HttpResponse
from .models import OrderInfo, OrderCommodity
from ..user.models import User, Address
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json


def order(request):
    if request.method == 'GET':
        return HttpResponse('XXX')

    # 获取选取情况
    com_key_lsit = [i for i in request.POST][1:]

    context = {}
    conn = get_redis_connection('default')
    this_id = request.session['info']['id']
    cart_id = 'cart_%d' % this_id

    # 运费
    freight = 10
    freight_id = 'freight_%d' % this_id
    conn.set(freight_id, freight)
    context['freight'] = freight

    # 商品总数
    com_all_num = conn.hlen(cart_id)
    context['com_all_num'] = com_all_num

    # 链接redis,查看缓存信息
    com_all = []
    com_all_id = conn.hgetall(cart_id)
    Count = 0

    if com_all_id:
        # 订单页面ID
        g = 1
        for i, j in com_all_id.items():
            temp = CommoditySKU.objects.filter(id=i)
            img = img_url(temp)[0]
            check_key = 'check_' + str(temp.first().id)
            if check_key in com_key_lsit:
                com_all.append([temp.first(), img, [int(j), int(j) * temp.first().price, g]])
                g += 1
                Count += int(j) * temp.first().price
        context['com_all'] = com_all
        context['count'] = Count
        context['allCount'] = Count + freight

    # 收件地址
    user_addr = Address.objects.filter(user_id=this_id)
    context['user_addr'] = user_addr

    # 将勾选记录放入redis中
    com_check_id = 'com_check_%d' % this_id
    conn.delete(com_check_id)
    for i in com_key_lsit:
        conn.sadd(com_check_id, i)

    return render(request, '../templates/place_order.html', context)


@csrf_exempt
def order_submit(request):
    print(request.POST)

    conn = get_redis_connection('default')
    this_id = request.session['info']['id']
    cart_id = 'cart_%d' % this_id
    com_check_id = 'com_check_%d' % this_id
    freight_id = 'freight_%d' % this_id

    # 链接redis,查看缓存信息
    com_all = []

    # 从redis总获取：商品总数，商品详情，购物车情况和运费
    com_all_id = conn.hgetall(cart_id)
    com_check_id = [str(i)[2:-1] for i in conn.smembers(com_check_id)]
    freight_id = conn.get(freight_id)
    Price, Count = 0, 0
    if com_all_id:
        # 创建订单ID:当前时间（年月日小时分秒 + X + 用户ID）
        timeId = datetime.now().strftime('%Y%m%d%H%M%S')
        trade_no = timeId + 'X' + str(request.session['info']['id'])
        xx = OrderInfo.objects.filter(trade_no=trade_no)

        rf = OrderInfo.objects.create(user_id=request.session['info']['id'],
                                      addr_id=request.POST['chk_value'],
                                      pay_method=request.POST['zhf_value'],
                                      total_count=Count,
                                      total_price=Price,
                                      transit_price=int(freight_id),
                                      trade_no=trade_no,
                                      )
        rf_id = OrderInfo.objects.filter(trade_no=trade_no).first().order_id
        rf.save()
        # 购物车信息加入订单
        for i, j in com_all_id.items():
            temp = CommoditySKU.objects.filter(id=i)
            check_key = 'check_' + str(temp.first().id)
            if check_key in com_check_id:
                if int(j) > temp.first().stock:
                    return HttpResponse('数量有误')
                one_com = OrderCommodity.objects.create(order_id=rf_id,
                                                        sku_id=int(i),
                                                        count=int(j),
                                                        price=int(j) * temp.first().price,
                                                        comment='xxx'
                                                        )
                one_com.save()
                Price += int(j) * temp.first().price
                Count += 1

        rf = OrderInfo.objects.filter(order_id=rf_id).update(total_count=Count, total_price=Price)
        conn.delete(cart_id,com_check_id,freight_id)


    return HttpResponse(json.dumps({'status': True}, ensure_ascii=False))
