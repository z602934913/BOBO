from django.shortcuts import render

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.list_mod_ult import img_url, text_and_img_list
from .models import IndexCommdityBanner, IndexPromotioinBanner, IndexTypeCommdityBanner, CommodityType, CommoditySKU, CommdityImage


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
        com_ty = [[i.logo, i.name] for i in com_type]
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


def detail(request, cid):
    com_all = CommoditySKU.objects.filter(id=cid)
    if not com_all:
        return HttpResponse('朋友，请别乱来')
    com_img = CommdityImage.objects.filter(sku=com_all.first())
    if not com_img:
        com_img = 'static/img/img/sorry.jpg'
    else:
        com_img = img_url(com_img)[0]
    return render(request, '../templates/detail.html', {'com_one': com_all.first(), 'com_img': com_img})
