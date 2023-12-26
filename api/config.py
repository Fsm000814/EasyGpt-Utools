# -*- coding:utf-8 -*-
import os
from datetime import timedelta
import dotenv
from extensions.ext_database import db
from extensions.ext_redis import redis_client

dotenv.load_dotenv()

DEFAULTS = {
    'DB_USERNAME': 'postgres',
    'DB_PASSWORD': '',
    'DB_HOST': 'localhost',
    'DB_PORT': '5432',
    'DB_DATABASE': 'easygpt',
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': '6379',
    'REDIS_DB': '0',
    'REDIS_USE_SSL': 'False',
    'OAUTH_REDIRECT_PATH': '/console/api/oauth/authorize',
    'OAUTH_REDIRECT_INDEX_PATH': '/',
    'CONSOLE_WEB_URL': 'https://cloud.dify.ai',
    'CONSOLE_API_URL': 'https://cloud.dify.ai',
    'SERVICE_API_URL': 'https://api.dify.ai',
    'APP_WEB_URL': 'https://udify.app',
    'APP_API_URL': 'https://udify.app',
    'FILES_URL': '',
    'STORAGE_TYPE': 'local',
    'STORAGE_LOCAL_PATH': 'storage',
    'CHECK_UPDATE_URL': 'https://updates.dify.ai',
    'DEPLOY_ENV': 'PRODUCTION',
    'SQLALCHEMY_POOL_SIZE': 30,
    'SQLALCHEMY_POOL_RECYCLE': 3600,
    'SQLALCHEMY_ECHO': 'False',
    'SENTRY_TRACES_SAMPLE_RATE': 1.0,
    'SENTRY_PROFILES_SAMPLE_RATE': 1.0,
    'WEAVIATE_GRPC_ENABLED': 'True',
    'WEAVIATE_BATCH_SIZE': 100,
    'CELERY_BACKEND': 'database',
    'LOG_LEVEL': 'INFO',
    'HOSTED_OPENAI_QUOTA_LIMIT': 200,
    'HOSTED_OPENAI_ENABLED': 'False',
    'HOSTED_OPENAI_PAID_ENABLED': 'False',
    'HOSTED_OPENAI_PAID_INCREASE_QUOTA': 1,
    'HOSTED_AZURE_OPENAI_ENABLED': 'False',
    'HOSTED_AZURE_OPENAI_QUOTA_LIMIT': 200,
    'HOSTED_ANTHROPIC_QUOTA_LIMIT': 600000,
    'HOSTED_ANTHROPIC_ENABLED': 'False',
    'HOSTED_ANTHROPIC_PAID_ENABLED': 'False',
    'HOSTED_ANTHROPIC_PAID_INCREASE_QUOTA': 1000000,
    'HOSTED_ANTHROPIC_PAID_MIN_QUANTITY': 20,
    'HOSTED_ANTHROPIC_PAID_MAX_QUANTITY': 100,
    'HOSTED_MODERATION_ENABLED': 'False',
    'HOSTED_MODERATION_PROVIDERS': '',
    'TENANT_DOCUMENT_COUNT': 100,
    'CLEAN_DAY_SETTING': 30,
    'UPLOAD_FILE_SIZE_LIMIT': 15,
    'UPLOAD_FILE_BATCH_LIMIT': 5,
    'UPLOAD_IMAGE_FILE_SIZE_LIMIT': 10,
    'OUTPUT_MODERATION_BUFFER_SIZE': 300,
    'MULTIMODAL_SEND_IMAGE_FORMAT': 'base64',
    'INVITE_EXPIRY_HOURS': 72
}

import os

def get_env(key):
    """
    获取环境变量的值。

    参数：
    key (str)：环境变量的键名。

    返回值：
    环境变量的值，如果环境变量不存在则返回默认值。

    引用：
    os.environ.get()：获取环境变量的值。
    DEFAULTS：默认值字典。
    """
    return os.environ.get(key, DEFAULTS.get(key))

def get_bool_env(key):
    """
    获取环境变量的布尔值。
    
    参数：
    key(str) -- 环境变量的键名
    
    返回值：
    bool -- 环境变量的布尔值，如果键名不存在或值不是'true'则返回False
    """
    return get_env(key).lower() == 'true'

def get_cors_allow_origins(env, default):
    """
    获取跨域允许的源列表

    Args:
        env (str): 环境变量
        default (str): 默认跨域允许的源

    Returns:
        list: 跨域允许的源列表
    """
    cors_allow_origins = []
    if get_env(env):
        for origin in get_env(env).split(','):
            cors_allow_origins.append(origin)
    else:
        cors_allow_origins = [default]

    return cors_allow_origins

class Config:
    """Application configuration class."""

    def __init__(self):
        """
        初始化函数
        """
        # ------------------------通用配置------------------------ 
        # 当前版本号
        self.CURRENT_VERSION = "0.3.31"
        # 代码提交的SHA值
        self.COMMIT_SHA = get_env('COMMIT_SHA')
        # 版本号
        self.EDITION = "SELF_HOSTED"
        # 部署环境
        self.DEPLOY_ENV = get_env('DEPLOY_ENV')
        # 测试模式开关
        self.TESTING = False
        # 日志级别
        self.LOG_LEVEL = get_env('LOG_LEVEL')

        # console API的后端URL前缀
        # 用于拼接登录授权回调或notion集成回调
        self.CONSOLE_API_URL = get_env('CONSOLE_URL') if get_env('CONSOLE_URL') else get_env('CONSOLE_API_URL')

        # console web的前端URL前缀
        # 用于拼接前端地址和用于CORS配置
        self.CONSOLE_WEB_URL = get_env('CONSOLE_URL') if get_env('CONSOLE_URL') else get_env('CONSOLE_WEB_URL')

        # WebApp API的后端URL前缀
        # 用于声明后端API的前端URL
        self.APP_API_URL = get_env('APP_URL') if get_env('APP_URL') else get_env('APP_API_URL')

        # WebApp的URL前缀
        # 用于向前端显示WebAPP API的基本URL
        self.APP_WEB_URL = get_env('APP_URL') if get_env('APP_URL') else get_env('APP_WEB_URL')

        # 服务API的URL前缀
        # 用于向前端显示服务API的基本URL
        self.SERVICE_API_URL = get_env('API_URL') if get_env('API_URL') else get_env('SERVICE_API_URL')

        # 文件预览或下载的URL前缀
        # 用于向前端或作为多模型输入显示文件预览或下载的URL；URL具有过期时间
        self.FILES_URL = get_env('FILES_URL') if get_env('FILES_URL') else self.CONSOLE_API_URL

        # 跳转URL前缀
        # 将被弃用
        self.CONSOLE_URL = get_env('CONSOLE_URL')
        self.API_URL = get_env('API_URL')
        self.APP_URL = get_env('APP_URL')

        # 应用的密钥将用于安全地签署会话cookie
        # 确保在部署之前更改密钥为强密钥
        # 您可以使用`openssl rand -base64 42`生成一个强密钥
        # 或者通过`SECRET_KEY`环境变量设置
        self.SECRET_KEY = get_env('SECRET_KEY')

        # CORS设置
        self.CONSOLE_CORS_ALLOW_ORIGINS = get_cors_allow_origins(
            'CONSOLE_CORS_ALLOW_ORIGINS', self.CONSOLE_WEB_URL)
        self.WEB_API_CORS_ALLOW_ORIGINS = get_cors_allow_origins(
            'WEB_API_CORS_ALLOW_ORIGINS', '*')

        # 检查更新的URL
        self.CHECK_UPDATE_URL = get_env('CHECK_UPDATE_URL')

        # ------------------------数据库配置------------------------ 
        # 数据库凭证
        db_credentials = {
            key: get_env(key) for key in
            ['DB_USERNAME', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_DATABASE']
        }

        # 数据库连接URL
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{db_credentials['DB_USERNAME']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_DATABASE']}"
        # 数据库引擎配置
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': int(get_env('SQLALCHEMY_POOL_SIZE')),
            'pool_recycle': int(get_env('SQLALCHEMY_POOL_RECYCLE'))
        }

        # SQL打印配置
        self.SQLALCHEMY_ECHO = get_bool_env('SQLALCHEMY_ECHO')

        # ------------------------Redis配置------------------------ 
        # Redis主机
        self.REDIS_HOST = get_env('REDIS_HOST')
        # Redis端口
        self.REDIS_PORT = get_env('REDIS_PORT')
        # Redis用户名
        self.REDIS_USERNAME = get_env('REDIS_USERNAME')
        # Redis密码
        self.REDIS_PASSWORD = get_env('REDIS_PASSWORD')
        # Redis数据库
        self.REDIS_DB = get_env('REDIS_DB')
        # Redis是否使用SSL
        self.REDIS_USE_SSL = get_bool_env('REDIS_USE_SSL')

        # ------------------------Celery工作线程配置------------------------ 
        # Celery工作线程URL
        self.CELERY_BROKER_URL = get_env('CELERY_BROKER_URL')
        # Celery后台
        self.CELERY_BACKEND = get_env('CELERY_BACKEND')
        # Celery结果后端
        self.CELERY_RESULT_BACKEND = 'db+{}'.format(self.SQLALCHEMY_DATABASE_URI) \
            if self.CELERY_BACKEND == 'database' else self.CELERY_BROKER_URL
        # 是否使用SSL连接broker
        self.BROKER_USE_SSL = self.CELERY_BROKER_URL.startswith('rediss://')

        # ------------------------文件存储配置------------------------ 
        # 存储类型
        self.STORAGE_TYPE = get_env('STORAGE_TYPE')
        # 存储本地路径
        self.STORAGE_LOCAL_PATH = get_env('STORAGE_LOCAL_PATH')
        # S3端点
        self.S3_ENDPOINT = get_env('S3_ENDPOINT')
        # S3 Bucket名称
        self.S3_BUCKET_NAME = get_env('S3_BUCKET_NAME')
        # S3访问密钥
        self.S3_ACCESS_KEY = get_env('S3_ACCESS_KEY')
        # S3安全密钥
        self.S3_SECRET_KEY = get_env('S3_SECRET_KEY')
        # S3区域
        self.S3_REGION = get_env('S3_REGION')

        # ------------------------向量存储配置------------------------ 
        # 向量存储
        self.VECTOR_STORE = get_env('VECTOR_STORE')

        # qdrant设置
        self.QDRANT_URL = get_env('QDRANT_URL')
        self.QDRANT_API_KEY = get_env('QDRANT_API_KEY')

        # milvus / zilliz设置
        self.MILVUS_HOST = get_env('MILVUS_HOST')
        self.MILVUS_PORT = get_env('MILVUS_PORT')
        self.MILVUS_USER = get_env('MILVUS_USER')
        self.MILVUS_PASSWORD = get_env('MILVUS_PASSWORD')
        self.MILVUS_SECURE = get_env('MILVUS_SECURE')

        # weaviate设置
        self.WEAVIATE_ENDPOINT = get_env('WEAVIATE_ENDPOINT')
        self.WEAVIATE_API_KEY = get_env('WEAVIATE_API_KEY')
        self.WEAVIATE_GRPC_ENABLED = get_bool_env('WEAVIATE_GRPC_ENABLED')
        self.WEAVIATE_BATCH_SIZE = int(get_env('WEAVIATE_BATCH_SIZE'))

        # ------------------------邮件配置------------------------ 
        # 邮件类型
        self.MAIL_TYPE = get_env('MAIL_TYPE')
        # 默认发送者
        self.MAIL_DEFAULT_SEND_FROM = get_env('MAIL_DEFAULT_SEND_FROM')
        # 重新发送API密钥
        self.RESEND_API_KEY = get_env('RESEND_API_KEY')

        # ------------------------工作空间配置------------------------ 
        # 邀请过期时间（小时）
        self.INVITE_EXPIRY_HOURS = int(get_env('INVITE_EXPIRY_HOURS'))

        # ------------------------Sentry配置------------------------ 
        # Sentry错误日志
        self.SENTRY_DSN = get_env('SENTRY_DSN')
        # Sentry跟踪率
        self.SENTRY_TRACES_SAMPLE_RATE = float(get_env('SENTRY_TRACES_SAMPLE_RATE'))
        # Sentry模型率
        self.SENTRY_PROFILES_SAMPLE_RATE = float(get_env('SENTRY_PROFILES_SAMPLE_RATE'))

        # ------------------------业务配置------------------------ 
        # 多模型发送图像格式，支持base64、url，默认为base64
        self.MULTIMODAL_SEND_IMAGE_FORMAT = get_env('MULTIMODAL_SEND_IMAGE_FORMAT')

        # 数据集配置
        self.TENANT_DOCUMENT_COUNT = get_env('TENANT_DOCUMENT_COUNT')
        # 清理天数设置
        self.CLEAN_DAY_SETTING = get_env('CLEAN_DAY_SETTING')

        # 文件上传配置
        # 上传文件大小限制（字节）
        self.UPLOAD_FILE_SIZE_LIMIT = int(get_env('UPLOAD_FILE_SIZE_LIMIT'))
        # 上传文件批大小限制（字节）
        self.UPLOAD_FILE_BATCH_LIMIT = int(get_env('UPLOAD_FILE_BATCH_LIMIT'))
        # 上传图片文件大小限制（字节）
        self.UPLOAD_IMAGE_FILE_SIZE_LIMIT = int(get_env('UPLOAD_IMAGE_FILE_SIZE_LIMIT'))

        # 隔离在应用中的配置
        self.OUTPUT_MODERATION_BUFFER_SIZE = int(get_env('OUTPUT_MODERATION_BUFFER_SIZE'))

        # 在应用中集成Notion设置
        self.NOTION_CLIENT_ID = get_env('NOTION_CLIENT_ID')
        self.NOTION_CLIENT_SECRET = get_env('NOTION_CLIENT_SECRET')
        self.NOTION_INTEGRATION_TYPE = get_env('NOTION_INTEGRATION_TYPE')
        self.NOTION_INTERNAL_SECRET = get_env('NOTION_INTERNAL_SECRET')
        self.NOTION_INTEGRATION_TOKEN = get_env('NOTION_INTEGRATION_TOKEN')

        # ------------------------平台配置------------------------ 
        # hosted OpenAI是否启用
        self.HOSTED_OPENAI_ENABLED = get_bool_env('HOSTED_OPENAI_ENABLED')
        # hosted OpenAI API密钥
        self.HOSTED_OPENAI_API_KEY = get_env('HOSTED_OPENAI_API_KEY')
        # hosted OpenAI API基础URL
        self.HOSTED_OPENAI_API_BASE = get_env('HOSTED_OPENAI_API_BASE')
        # hosted OpenAI API组织限制
        self.HOSTED_OPENAI_API_ORGANIZATION = get_env('HOSTED_OPENAI_API_ORGANIZATION')
        # hosted OpenAI配额限制
        self.HOSTED_OPENAI_QUOTA_LIMIT = int(get_env('HOSTED_OPENAI_QUOTA_LIMIT'))
        # 是否付费启用hosted OpenAI
        self.HOSTED_OPENAI_PAID_ENABLED = get_bool_env('HOSTED_OPENAI_PAID_ENABLED')
        # hosted OpenAI定价API
        self.HOSTED_OPENAI_PAID_STRIPE_PRICE_ID = get_env('HOSTED_OPENAI_PAID_STRIPE_PRICE_ID')
        # 增加配额
        self.HOSTED_OPENAI_PAID_INCREASE_QUOTA = int(get_env('HOSTED_OPENAI_PAID_INCREASE_QUOTA'))

        # hosted Azure OpenAI是否启用
        self.HOSTED_AZURE_OPENAI_ENABLED = get_bool_env('HOSTED_AZURE_OPENAI_ENABLED')
        # 设置 HOSTED_AZURE_OPENAI_API_KEY
        self.HOSTED_AZURE_OPENAI_API_KEY = get_env('HOSTED_AZURE_OPENAI_API_KEY')
        # 设置 HOSTED_AZURE_OPENAI_API_BASE
        self.HOSTED_AZURE_OPENAI_API_BASE = get_env('HOSTED_AZURE_OPENAI_API_BASE')
        # 设置 HOSTED_AZURE_OPENAI_QUOTA_LIMIT
        self.HOSTED_AZURE_OPENAI_QUOTA_LIMIT = int(get_env('HOSTED_AZURE_OPENAI_QUOTA_LIMIT'))

        # 设置是否启用 HOSTED_ANTHROPIC_ENABLED
        self.HOSTED_ANTHROPIC_ENABLED = get_bool_env('HOSTED_ANTHROPIC_ENABLED')
        # 设置 HOSTED_ANTHROPIC_API_BASE
        self.HOSTED_ANTHROPIC_API_BASE = get_env('HOSTED_ANTHROPIC_API_BASE')
        # 设置 HOSTED_ANTHROPIC_API_KEY
        self.HOSTED_ANTHROPIC_API_KEY = get_env('HOSTED_ANTHROPIC_API_KEY')
        # 设置 HOSTED_ANTHROPIC_QUOTA_LIMIT
        self.HOSTED_ANTHROPIC_QUOTA_LIMIT = int(get_env('HOSTED_ANTHROPIC_QUOTA_LIMIT'))
        # 设置是否启用 HOSTED_ANTHROPIC_PAID_ENABLED
        self.HOSTED_ANTHROPIC_PAID_ENABLED = get_bool_env('HOSTED_ANTHROPIC_PAID_ENABLED')
        # 设置 HOSTED_ANTHROPIC_PAID_STRIPE_PRICE_ID
        self.HOSTED_ANTHROPIC_PAID_STRIPE_PRICE_ID = get_env('HOSTED_ANTHROPIC_PAID_STRIPE_PRICE_ID')
        # 设置 HOSTED_ANTHROPIC_PAID_INCREASE_QUOTA
        self.HOSTED_ANTHROPIC_PAID_INCREASE_QUOTA = int(get_env('HOSTED_ANTHROPIC_PAID_INCREASE_QUOTA'))
        # 设置 HOSTED_ANTHROPIC_PAID_MIN_QUANTITY
        self.HOSTED_ANTHROPIC_PAID_MIN_QUANTITY = int(get_env('HOSTED_ANTHROPIC_PAID_MIN_QUANTITY'))
        # 设置 HOSTED_ANTHROPIC_PAID_MAX_QUANTITY
        self.HOSTED_ANTHROPIC_PAID_MAX_QUANTITY = int(get_env('HOSTED_ANTHROPIC_PAID_MAX_QUANTITY'))

        # 设置是否启用 HOSTED_MODERATION_ENABLED
        self.HOSTED_MODERATION_ENABLED = get_bool_env('HOSTED_MODERATION_ENABLED')
        # 设置 HOSTED_MODERATION_PROVIDERS
        self.HOSTED_MODERATION_PROVIDERS = get_env('HOSTED_MODERATION_PROVIDERS')
