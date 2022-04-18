from django.db import models
from utils.baseModel import BaseModel
from apps import user, commodity


class OrderInfo(BaseModel):
    '''订单表'''

    order_id = models.AutoField(verbose_name='订单ID', primary_key=True, auto_created=True)
    user = models.ForeignKey(verbose_name='所属用户', to='user.User', on_delete=models.CASCADE)
    addr = models.ForeignKey(verbose_name='用户地址', to='user.Address', on_delete=models.CASCADE)

    pey_method_choices = (
        (1, '微信'),
        (2, '支付宝'),
        (3, '云闪付'),
        (4, '银联')
    )
    pay_method = models.SmallIntegerField(verbose_name='支付方式', choices=pey_method_choices, default=1)
    total_count = models.IntegerField(verbose_name='商品数量', default=1)
    total_price = models.DecimalField(verbose_name='商品金额', max_digits=10, decimal_places=2)
    transit_price = models.DecimalField(verbose_name='运费', max_digits=10, decimal_places=2)

    order_status_choices = (
        (1, '待支付'),
        (2, '代发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )
    order_status = models.SmallIntegerField(verbose_name='订单状况', choices=order_status_choices, default=1)
    trade_no = models.CharField(verbose_name='订单编号', max_length=128)

    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.trade_no)

class OrderCommodity(BaseModel):
    '''订单商品表'''
    order = models.ForeignKey(verbose_name='订单号', to='OrderInfo', on_delete=models.CASCADE)
    sku = models.ForeignKey(verbose_name='商品SKU', to='commodity.CommoditySKU', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='商品数目', default=1)
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    comment = models.CharField(verbose_name='评论', max_length=246)

    class Meta:
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.trade_no) + self.sku.name