from django.db import models
from utils.baseModel import BaseModel
from tinymce.models import HTMLField

class CommodityType(BaseModel):
    '''商品类型表'''
    name = models.CharField(verbose_name='商品名',max_length=20)
    logo = models.CharField(verbose_name='标识',max_length=100)
    image = models.ImageField(verbose_name='展示图',max_length=100,upload_to='apps/commodity/static/img/type')

    def __str__(self):
        return self.name

    class Meta:
        # db_table = 'df_Commodity_Type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name


class CommoditySKU(BaseModel):
    '''商品SKU表'''
    type = models.ForeignKey(verbose_name='商品类型',to='CommodityType',on_delete=models.CASCADE)
    commodities = models.ForeignKey(verbose_name='商品SPU',to='Commodity',on_delete=models.CASCADE)
    name = models.CharField(verbose_name='商品名称',max_length=20)
    desc = models.CharField(verbose_name='商品简介',max_length=200)
    price = models.DecimalField(verbose_name='商品价格',max_digits=10,decimal_places=2)
    untie = models.CharField(verbose_name='商品单位',max_length=20)
    image = models.ImageField(verbose_name='商品图片',upload_to='apps/commodity/static/img/SKU')
    stock = models.IntegerField(verbose_name='商品库存',default=1)
    sales = models.IntegerField(verbose_name='商品销量',default=0)

    status_choices = (
        (0,'上架'),
        (1,'下架')
    )

    status = models.SmallIntegerField(verbose_name='上架情况',default=1,choices=status_choices)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'df_Commodity_SKU'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name


class Commodity(BaseModel):
    '''商品SPU表'''
    name = models.CharField(verbose_name='商品SPU名称',max_length=20)
    detail = models.TextField(verbose_name='商品详情',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'df_Commodity'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name



class CommdityImage(BaseModel):
    '''商品图片表'''
    sku = models.ForeignKey(verbose_name='商品',to='CommoditySKU',on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='图片路径',upload_to='apps/commodity/static/img/img')

    class Meta:
        db_table = 'df_Commodity_Image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.sku.name


class IndexCommdityBanner(BaseModel):
    '''首页轮播商品表'''
    sku = models.ForeignKey(verbose_name='商品',to='CommoditySKU',on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='图片路径',upload_to='apps/commodity/static/img/banner')
    index = models.SmallIntegerField(verbose_name='展示顺序',default=0)

    class Meta:
        db_table = 'df_Index_Commodity_Banner'
        verbose_name = '首页轮播商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.index)


class IndexTypeCommdityBanner(BaseModel):
    '''首页分类商品展示表'''
    sku = models.ForeignKey(verbose_name='商品',to='CommoditySKU',on_delete=models.CASCADE)
    display_choices = (
        (0,'文字'),
        (1,'图片')
    )
    display_type = models.SmallIntegerField(verbose_name='展示类型',default=1,choices=display_choices)
    index = models.SmallIntegerField(verbose_name='展示顺序',default=0)

    def __str__(self):
        return str(self.sku.name) + str(self.index) + str(self.display_type)

    class Meta:
        db_table = 'df_Index_Type_Commodity_Banner'
        verbose_name = '首页分类商品展示表'
        verbose_name_plural = verbose_name


class IndexPromotioinBanner(BaseModel):
    '''首页促销活动类型表'''
    name = models.CharField(verbose_name='活动名称',max_length=20)
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(verbose_name='活动图片',upload_to='apps/commodity/static/img/Promotionin')
    index = models.SmallIntegerField(verbose_name='展示顺序',default=0)

    def __str__(self):
        return  self.name

    class Meta:
        db_table = 'df_Index_Promotionin_Banner'
        verbose_name = '首页促销活动类型表'
        verbose_name_plural = verbose_name
