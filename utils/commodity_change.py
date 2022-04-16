from django.http import HttpResponse

import json

from django.http import HttpResponse
from django_redis import get_redis_connection

from apps.commodity.models import CommoditySKU


def commdity_change(request,dc=1):
    """传入request,
    am为1时为增加1(或其他)，为2时为减少1；
    dc为购物车页面或商品页面：1时为商品2为购物车"""

    # 获取ajax传递过来的信息，com_id:商品ID, now_num:商品数量
    com_id = request.POST['com_id']
    now_num = int(request.POST['now_num'])

    # 链接redis
    conn = get_redis_connection('default')

    if request.session['info']['id']:

        # 获取用户购物车ID，购物车状态,商品库存量,
        cart_key = 'cart_%d' % request.session['info']['id']
        cart_res = int(conn.hget(cart_key,com_id)) if conn.hget(cart_key,com_id) else 0
        com = CommoditySKU.objects.filter(id=com_id).first()
        stock = -1 if not com else int(com.stock)

        # 当为购物车页面时，总量设置为当前量，当为商品页面的时候，总量设为两者之和
        if dc == 1:
            order_num = cart_res + now_num
        else:
            order_num = now_num

        # 判断添加数量是否正确
        if stock == -1:
            return HttpResponse(json.dumps({'status':False,'im':'添加数量有误'}, ensure_ascii=False))
        elif now_num > stock and dc == 1:
            return HttpResponse(json.dumps({'status':False,'im':'添加数量有误'}, ensure_ascii=False))
        elif order_num > stock:
            order_num = stock

        # 当购物车不存在该商品时
        if not cart_res:
            add_res = conn.hset(cart_key, com_id, order_num)
            if add_res == 1:
                data_dict = {'status': True, 'im':'添加成功'}
                return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

        # 当商品存在的时候
        add_res = conn.hset(cart_key, com_id, order_num)
        if add_res == 0:
            data_dict = {'status': True, 'im': '添加成功'}
            return json.dumps(data_dict, ensure_ascii=False)