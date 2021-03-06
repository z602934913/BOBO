from django.db import models
from datetime import datetime

class BaseModel(models.Model):
    '''模型基类'''
    create_times = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,verbose_name='删除标签')

    class Meta:
        abstract = True
