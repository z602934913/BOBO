def img_url(order_list):
    return ["/".join(i.split('/')[2:]) for i in [str(i.image) for i in order_list]]


def text_and_img_list(text_list, img_list):
    '''输入 文字表达的总类，图片表达的总类
        输出 文字类的(id,名称)，图片类的（id,名称，路径，价格）'''
    com_01_id_name = [[i.sku.id,i.sku.commodities.name] for i in img_list]
    com_01_url = img_url([i.sku for i in img_list])
    com_01_pri = [i.sku.price for i in img_list]
    com_01 = [i+[j, k] for i, j, k in zip(com_01_id_name, com_01_url, com_01_pri)]
    com_02 = [(i.sku.id, i.sku.name) for i in text_list]
    return com_02, com_01
