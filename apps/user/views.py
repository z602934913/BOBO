from io import BytesIO

from django.core import mail
from django.core.cache import cache
from django.shortcuts import render,redirect
from django.http import HttpResponse

from utils.code import check_code
from utils.encrypt import SecretOauth
from utils.form import RegisterModelForm, LoginModelForm
from .models import User
from utils.encrypt import md5


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
        return redirect('/user/login')

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


def login(request):
    if request.method == 'GET':
        form = LoginModelForm()
        return render(request,'../templates/login.html',{'form':form})
    form = LoginModelForm(data=request.POST)
    # 验证码的校验
    user_input_code = request.POST['code']
    code = request.session.get('image_code', "")
    if code.upper() != user_input_code.upper() or code == '':
        code_error = '大兄弟，验证码错误'
        return render(request, 'login.html', {'form': form,'code_error':code_error},)
    admin_object = User.objects.filter(username=request.POST['username'],password=md5(request.POST['password'])).first()
    if not admin_object:
        form.add_error("password", "同志，用户名或密码错咯！")
        return render(request, 'login.html', {'form': form})
    request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
    request.session.set_expiry(60 * 60 * 24 * 7)
    return redirect('/user/user_center_info')

    # return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()
    return redirect('/user/login')

def user_center_info(request):
    return render(request,'user_center_info.html')


def user_center_oredr(request):
    return render(request,'user_center_order.html')


def user_center_site(request):
    return render(request,'user_center_site.html')