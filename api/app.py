from flask import Flask # 导入flask框架
from config import Config # 导入配置
import logging  # 导入日志模块
import os  # 导入操作系统模块
from extensions import  ext_redis, ext_login, ext_migrate, ext_database, ext_storage, ext_mail, ext_code_based_extension
# ext_celery, ext_sentry,ext_stripe
from core.model_providers.providers import hosted
from flask_cors import CORS
# fix windows platform
if os.name == "nt":  # 如果操作系统为Windows
    os.system('tzutil /s "UTC"')  # 执行命令'tzutil /s "UTC"'
else:  # 如果操作系统不是Windows
    os.environ['TZ'] = 'UTC'  # 设置TZ环境变量为'UTC'
    time.tzset()  # 设置时间时区

class EasyGptApp(Flask):
    pass


# -------------
# Configuration
# -------------

app = EasyGptApp(__name__)

# ----------------------------
# Application Factory Function
# ----------------------------

def create_app() -> Flask:
    
    app = EasyGptApp(__name__)

    # 获取配置
    app.config.from_object(Config())

    app.secret_key = app.config['SECRET_KEY']

    logging.basicConfig(level=app.config.get('LOG_LEVEL', 'INFO'))

    initialize_extensions(app)
    # 注册蓝图 Cors处理
    # register_blueprints(app)

    # 注册命令
    # register_commands(app)

    hosted.init_app(app)

    return app

def initialize_extensions(app):
    # 基础扩展
    ext_code_based_extension.init()
    # 数据库扩展
    ext_database.init_app(app)
    # 迁移扩展
    ext_migrate.init(app, db)
    # redis扩展
    ext_redis.init_app(app)
    # 存储扩展
    ext_storage.init_app(app)
    # 同步任务扩展
    # ext_celery.init_app(app)
    # 登录扩展
    ext_login.init_app(app)
    # 邮件扩展
    # ext_mail.init_app(app)
    # 异常捕获扩展
    # ext_sentry.init_app(app)
    # 支付扩展
    # ext_stripe.init_app(app)

# def register_blueprints(app):
#     """
#     注册蓝图函数

#     :param app: Flask应用对象
#     """
#     from controllers.service_api import bp as service_api_bp  # 服务API控制器蓝图
#     from controllers.web import bp as web_bp  # Web控制器蓝图
#     from controllers.console import bp as console_app_bp  # 控制台控制器蓝图
#     from controllers.files import bp as files_bp  # 文件控制器蓝图

#     CORS(service_api_bp,  # 为服务API蓝图启用跨域资源共享
#          allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],  # 允许的请求头部
#          methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH']  # 允许的请求方法
#          )
#     app.register_blueprint(service_api_bp)  # 注册服务API蓝图

#     CORS(web_bp,  # 为Web控制器蓝图启用跨域资源共享
#          resources={  # 资源限制
#              r"/*": {"origins": app.config['WEB_API_CORS_ALLOW_ORIGINS']}  # 允许的请求源
#          },
#          supports_credentials=True,  # 是否允许包含凭证
#          allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],  # 允许的请求头部
#          methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],  # 允许的请求方法
#          expose_headers=['X-Version', 'X-Env']  # 允许的响应头部
#          )

#     app.register_blueprint(web_bp)  # 注册Web控制器蓝图

#     CORS(console_app_bp,  # 为控制台控制器蓝图启用跨域资源共享
#          resources={  # 资源限制
#              r"/*": {"origins": app.config['CONSOLE_CORS_ALLOW_ORIGINS']}  # 允许的请求源
#          },
#          supports_credentials=True,  # 是否允许包含凭证
#          allow_headers=['Content-Type', 'Authorization'],  # 允许的请求头部
#          methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],  # 允许的请求方法
#          expose_headers=['X-Version', 'X-Env']  # 允许的响应头部
#          )

#     app.register_blueprint(console_app_bp)  # 注册控制台控制器蓝图

#     CORS(files_bp,  # 为文件控制器蓝图启用跨域资源共享
#          allow_headers=['Content-Type'],  # 允许的请求头部
#          methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH']  # 允许的请求方法
#          )
#     app.register_blueprint(files_bp)  # 注册文件控制器蓝图
# @app.route('/')
# def home():
#     return 'Hello, World!'