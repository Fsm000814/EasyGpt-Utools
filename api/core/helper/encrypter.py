import base64

from extensions.ext_database import db
from libs import rsa

# from models.account import Tenant


def obfuscated_token(token: str):
    """混淆token，将除了前六个字符和后两个字符以外的字符替换为*"""
    return token[:6] + '*' * (len(token) - 8) + token[-2:]


# def encrypt_token(tenant_id: str, token: str):
#     """使用租户的公钥加密token并返回编码后的字符串"""
#     tenant = db.session.query(Tenant).filter(Tenant.id == tenant_id).first()
#     encrypted_token = rsa.encrypt(token, tenant.encrypt_public_key)
#     return base64.b64encode(encrypted_token).decode()


def decrypt_token(tenant_id: str, token: str):
    """使用租户的私钥解密token并返回解密后的字符串"""
    return rsa.decrypt(base64.b64decode(token), tenant_id)