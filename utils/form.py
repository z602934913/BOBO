from apps.user.models import *
from apps.order.models import *
from apps.commodity.models import *

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.encrypt import md5


class BootStrap:
    '''重定义基类表单'''

    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                # field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    # "class": "form-control",
                    "placeholder": field.label
                }

class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass

class RegisterModelForm(BootStrapModelForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(),
        required=True
    )

    class Meta:
        model = User
        fields = ['username','password','confirm_password','email']

    def clean_username(self):
        name = self.cleaned_data.get('username')
        filt_name = User.objects.filter(username=name)
        if filt_name:
            raise ValidationError('用户名已存在')
        return name

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != md5(confirm_password):
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


class LoginModelForm(forms.ModelForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True,
        error_messages={
            'required': '小伙子，用户名和密码都不能为空啊！'
        }
    )
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if name == 'username':
                field.widget.attrs = {
                    "class": "name_input",
                    "placeholder": field.label
                }
            elif name == 'password':
                field.widget.attrs = {
                    "class": "pass_input",
                    "placeholder": field.label
                }

    class Meta:
        model = User
        fields = ['username','password']


