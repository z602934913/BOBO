from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.baseModel import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


class User(AbstractUser,BaseModel):
    '''用户表'''

    activate_choices = (
        (0,'未激活'),
        (1,'已激活')
    )
    is_active = models.BooleanField(verbose_name='激活状态',default=0,choices=activate_choices)

    def generate_active_token(self):
        '''签名字符串'''
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':self.id}
        token = serializer.dumps(info)
        return token.decode()


class Address(BaseModel):
    '''地址表'''
    user = models.ForeignKey(verbose_name='所属账户',to='User',on_delete=models.CASCADE)
    receiver = models.CharField(verbose_name='收件人',max_length=20)
    addr = models.CharField(verbose_name='收件地址',max_length=256)
    zip_code = models.CharField(verbose_name='邮政编码',null=True,max_length=6)
    phone = models.CharField(verbose_name='联系电话',max_length=11)
    is_default = models.BooleanField(verbose_name='默认地址？',default=False)




