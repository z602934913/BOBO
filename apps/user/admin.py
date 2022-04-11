from django.contrib import admin
from django.shortcuts import HttpResponse
# Register your models here.

def test_01(request):
    return HttpResponse('1111')