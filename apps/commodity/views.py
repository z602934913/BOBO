import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from utils.list_mod_ult import img_url, text_and_img_list
from .models import IndexCommdityBanner, IndexPromotioinBanner, IndexTypeCommdityBanner, CommodityType, CommoditySKU, \
    CommdityImage

from utils.pagination import Pagination


def index(request):
    if request.method == 'GET':
        context = {}
        # 首页轮播表
        com_banner = img_url(IndexCommdityBanner.objects.all().order_by('index'))
        context['com_banner'] = com_banner

        # 活动表
        com_pro = IndexPromotioinBanner.objects.all().order_by('index')
        com_pro1 = img_url(com_pro)
        context['com_pro1'] = com_pro1

        # 分类展示总图
        com_type = CommodityType.objects.all().order_by('logo')
        com_ty = [[i.logo, i.name, i.id] for i in com_type]
        com_ty_url = img_url(com_type)
        [i.append(j) for i, j in zip(com_ty, com_ty_url)]

        # 分类展示
        for i, j in zip(com_type, com_ty):
            com_ty_ba_01 = IndexTypeCommdityBanner.objects.filter(display_type=1, sku__type__id=i.id).order_by('index')
            com_ty_ba_02 = IndexTypeCommdityBanner.objects.filter(display_type=0, sku__type__id=i.id).order_by('index')
            com_tb02, com_tb01 = text_and_img_list(com_ty_ba_02, com_ty_ba_01)
            '''text:(id,名称）， img:(id,名称，图片url,价格)'''
            j.append([com_tb01, com_tb02])

        context['com_ty'] = com_ty

        return render(request, '../templates/index.html', context)


def detail(request, cid=0):
    # 没有商品ID则返回首页
    if cid == 0:
        return redirect('../')
    com_all = CommoditySKU.objects.filter(id=cid)
    if not com_all:
        return HttpResponse('朋友，请别乱来')
    com_img = CommdityImage.objects.filter(sku=com_all.first())

    # 若图片不存在
    com_img = 'static/img/img/sorry.jpg' if not com_img else img_url(com_img)[0]

    # 新品推荐部分
    # 随机
    new_com = CommoditySKU.objects.all().order_by('create_times')
    ran = []
    while len(ran) < 2:
        dd = random.randint(0, len(new_com) - 1)
        if dd not in ran:
            ran.append(dd)

    new_com = [new_com[i] for i in ran]
    new_img = img_url(new_com)

    # 记录用户浏览记录
    if request.session['info']:
        conn = get_redis_connection('default')
        # 添加到浏览记录中且保持浏览记录数量为4
        history_key = 'history_%d' % request.session['info']['id']
        conn.lrem(history_key, 0, cid)
        conn.lpush(history_key, cid)
        conn.ltrim(history_key, 0, 4)

    return render(request, '../templates/detail.html',
                  {'com_one': com_all.first(), 'com_img': com_img, 'new_img': new_img, 'new_com': new_com})


def all_list(request):
    tid = 0 if 'type' not in request.GET else request.GET['type']
    aid = 1 if 'pa' not in request.GET else request.GET['pa']
    pid = 1 if 'page' not in request.GET else request.GET['page']
    if tid == 0:
        return redirect('http://127.0.0.1:8000/index')

    # 根据默认，价格，人气进行排序
    if aid == str(1):
        all_com = CommoditySKU.objects.filter(type_id=tid).order_by('create_times')
    elif aid == str(2):
        all_com = CommoditySKU.objects.filter(type_id=tid).order_by('price')
    else:
        all_com = CommoditySKU.objects.filter(type_id=tid).order_by('sales')

    page_obj = Pagination(request, all_com, 5, )
    page_obj_img = img_url(page_obj.page_queryset)
    # [分页数据，图片url]
    page_com = [[i, j] for i, j in zip(page_obj.page_queryset, page_obj_img)]
    context = {"page_com": page_com, "page_string": page_obj.html(), 'aid': aid}

    # 新品推荐部分(随机)
    ran = []
    if len(all_com) >= 2:
        while len(ran) < 2:
            dd = random.randint(0, len(all_com) - 1)
            if dd not in ran:
                ran.append(dd)

    new_com = [all_com[i] for i in ran]
    new_img = img_url(new_com)
    context['new_img'] = new_img
    context['new_com'] = new_com

    return render(request, '../templates/list.html', context)
