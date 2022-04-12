from django.shortcuts import render
from django.http import HttpResponse
from utils.form import RegisterModelForm
from django.shortcuts import render, redirect
from django.core.cache import cache
from utils.encrypt import SecretOauth
from .models import User
from django.core import mail

def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request,'../templates/register_01.html',{'form':form})

    form = RegisterModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        dd = SecretOauth().dumps(request.POST['username'])
        cache.set(request.POST['username'],str(dd),3600)


        #邮件发送
        text = '你好，激活邮件如下\n' + 'http://127.0.0.1:8000/user/activate/' + dd + '\n 感谢您注册'
        recipient = request.POST['email']
        mail.send_mail(
            subject='天天生鲜激活',
            message=text,
            from_email='expcman@163.com',
            recipient_list=[str(recipient)]
        )
        # return redirect()

    return render(request, '../templates/register_01.html', {'form': form})


def activate(request,nid):
    dd = SecretOauth().loads(nid)
    user = User.objects.filter(username=dd)
    if not dd or not user:
        return render(request,'../templates/activate.html',{'title':'激活链接有误或已过期'})
    user = user[0]
    if user.is_active == 1:
        return render(request, '../templates/activate.html', {'title': '请勿重复激活'})
    user.is_active = 1
    user.save()
    cache.delete_pattern(dd)
    return render(request, '../templates/activate.html', {'title': '已激活'})
