"""django_BOBO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from apps.user import admin
from django.contrib import admin
from apps.user import views as u_v
from apps.commodity import views as c_v
from apps.cart import views as a_c
from apps.order import views as o_v
import tinymce

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('gogogo/',admin.test_01),
    path('tinymce/', include('tinymce.urls')),

    # 注册界面
    path('user/register', u_v.register),
    path('user/activate/<str:nid>', u_v.activate),

    # 登录界面
    path('user/login', u_v.login),
    path('user/code', u_v.image_code),
    path('user/logout', u_v.logout),

    # 用户界面,
    path('user/user_center_info', u_v.user_center_info),
    path('user/user_center_order', u_v.user_center_order),
    path('user/user_center_site', u_v.user_center_site),

    # 商品首页
    path('index/', c_v.index),
    path('index/detail/<str:cid>', c_v.detail),
    path('index/detail/', c_v.detail),
    path('index/list', c_v.all_list),
    # path('index/list/?type=<str:tid>', c_v.all_list),
    path('index/list/add_cart', c_v.add_cart),

    # 购物车页面
    path('cart/', a_c.cart),
    path('cart/change', a_c.cart_change),
    path('cart/del', a_c.cart_del),

    # 订单页面
    path('order/',o_v.order),
    path('order/submit', o_v.order_submit),

]
