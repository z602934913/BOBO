from django.shortcuts import render
from django_redis import get_redis_connection

def cart(request):
    conn = get_redis_connection()

    return render(request,'../templates/cart.html')
