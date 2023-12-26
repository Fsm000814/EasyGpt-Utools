# -*- coding:utf-8 -*-
import jwt
from werkzeug.exceptions import Unauthorized
from flask import current_app
class PassportService:
    def __init__(self):
        self.sk = current_app.config.get('SECRET_KEY')
    
    def issue(self, payload):
        """
        issue方法用于生成jwt令牌。
        
        Args:
            payload: dict, 包含需要编码的用户数据。
        
        Returns:
            str, 编码后的jwt令牌。
        """
        return jwt.encode(payload, self.sk, algorithm='HS256')
    
    def verify(self, token):
        """
        验证令牌是否有效

        Args:
            token (str): 要验证的令牌

        Returns:
            tuple: 验证通过后的解码结果

        Raises:
            Unauthorized: 令牌签名无效时抛出
            Unauthorized: 令牌无效时抛出
            Unauthorized: 令牌已过期时抛出
        """
        try:
            return jwt.decode(token, self.sk, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorized('Invalid token signature.')
        except jwt.exceptions.DecodeError:
            raise Unauthorized('Invalid token.')
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorized('Token has expired.')
