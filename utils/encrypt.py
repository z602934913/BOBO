from django.conf import settings
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


# 需要安装pip install itsdangerous
# 自己设置的秘钥
expires_in = None #如果是None默认3600，可以自己设置时间，单位(s),eg:3600


class SecretOauth(object):
    def __init__(self):
        self.serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=expires_in)

    # 加密
    def dumps(self, content_dict):
        token = self.serializer.dumps(content_dict).decode()
        return token

    # 解密
    def loads(self, token):
        try:
            content_dict = self.serializer.loads(token)
        except:
            content_dict = None
        return content_dict


