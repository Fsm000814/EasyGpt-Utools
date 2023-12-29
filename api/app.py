from flask import Flask, request, Response # 从flask模块中导入Flask类、request对象和Response类
from config import Config # 导入配置
from werkzeug.exceptions import Unauthorized  # 导入未经授权的异常
import logging  # 导入日志模块
import json  # 导入JSON模块
import os  # 导入操作系统模块
from extensions import  ext_redis, ext_login, ext_migrate, ext_database, ext_storage, ext_mail, ext_code_based_extension # 从extensions模块中导入相应的扩展
from extensions.ext_database import db  # 从extensions.ext_database模块中导入db
from extensions.ext_login import login_manager  # 从extensions.ext_login模块中导入login_manager
# ext_celery, ext_sentry,ext_stripe
# from core.model_providers.providers import hosted # 从core.model_providers.providers模块中导入hosted
from flask_cors import CORS # 从flask_cors模块中导入CORS类
from libs.passport import PassportService  # 从libs.passport模块中导入PassportService类
# fix windows platform
if os.name == "nt":  # 如果操作系统为Windows
    os.system('tzutil /s "UTC"')  # 执行命令'tzutil /s "UTC"'
else:  # 如果操作系统不是Windows
    os.environ['TZ'] = 'UTC'  # 设置TZ环境变量为'UTC'
    time.tzset()  # 设置时间时区

class EasyGptApp(Flask):
    pass

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

    # 宿主模型配置
    # hosted.init_app(app)

    return app

def initialize_extensions(app):
    # 基础扩展
    # ext_code_based_extension.init()
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
    # ext_login.init_app(app)
    # 邮件扩展
    # ext_mail.init_app(app)
    # 异常捕获扩展
    # ext_sentry.init_app(app)
    # 支付扩展
    # ext_stripe.init_app(app)

@login_manager.request_loader
def load_user_from_request(request_from_flask_login):
    """根据请求加载用户."""
    if request.blueprint == 'console':
        # 检查用户_id是否包含点号，指示旧格式
        auth_header = request.headers.get('Authorization', '')
        if ' ' not in auth_header:
            raise Unauthorized('无效的Authorization标头格式。期望格式为\'Bearer <api-key>\'。')
        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != 'bearer':
            raise Unauthorized('无效的Authorization标头格式。期望格式为\'Bearer <api-key>\'。')
        
        decoded = PassportService().verify(auth_token)
        user_id = decoded.get('user_id')

        # return AccountService.load_user(user_id)
        return None
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    处理未授权的请求。

    返回一个401未授权状态码的响应，响应内容为一个JSON对象，包含错误代码和错误信息。
    """
    return Response(json.dumps({
        'code': 'unauthorized',
        'message': "Unauthorized."
    }), status=401, content_type="application/json")

def register_blueprints(app):
    """
    注册蓝图函数

    :param app: Flask应用对象
    """
    from controllers.service_api import bp as service_api_bp  # 服务API控制器蓝图
    from controllers.web import bp as web_bp  # Web控制器蓝图
    from controllers.console import bp as console_app_bp  # 控制台控制器蓝图
    from controllers.files import bp as files_bp  # 文件控制器蓝图

    CORS(service_api_bp,  # 为服务API蓝图启用跨域资源共享
         allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],  # 允许的请求头部
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH']  # 允许的请求方法
         )
    app.register_blueprint(service_api_bp)  # 注册服务API蓝图

    CORS(web_bp,  # 为Web控制器蓝图启用跨域资源共享
         resources={  # 资源限制
             r"/*": {"origins": app.config['WEB_API_CORS_ALLOW_ORIGINS']}  # 允许的请求源
         },
         supports_credentials=True,  # 是否允许包含凭证
         allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],  # 允许的请求头部
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],  # 允许的请求方法
         expose_headers=['X-Version', 'X-Env']  # 允许的响应头部
         )

    app.register_blueprint(web_bp)  # 注册Web控制器蓝图

    CORS(console_app_bp,  # 为控制台控制器蓝图启用跨域资源共享
         resources={  # 资源限制
             r"/*": {"origins": app.config['CONSOLE_CORS_ALLOW_ORIGINS']}  # 允许的请求源
         },
         supports_credentials=True,  # 是否允许包含凭证
         allow_headers=['Content-Type', 'Authorization'],  # 允许的请求头部
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],  # 允许的请求方法
         expose_headers=['X-Version', 'X-Env']  # 允许的响应头部
         )

    app.register_blueprint(console_app_bp)  # 注册控制台控制器蓝图

    CORS(files_bp,  # 为文件控制器蓝图启用跨域资源共享
         allow_headers=['Content-Type'],  # 允许的请求头部
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH']  # 允许的请求方法
         )
    app.register_blueprint(files_bp)  # 注册文件控制器蓝图

app = create_app()
# celery = app.extensions["celery"]

if app.config['TESTING']:
    print("App is running in TESTING mode")

@app.after_request
def after_request(response):
    """在响应结束后添加版本头到响应中。"""
    response.set_cookie('remember_token', '', expires=0)
    response.headers.add('X-Version', app.config['CURRENT_VERSION'])
    response.headers.add('X-Env', app.config['DEPLOY_ENV'])
    return response

@app.route('/health')
def health():
    """
    健康检查函数，返回一个包含状态码200和应用配置信息的JSON响应

    :return: JSON响应对象
    """
    return Response(json.dumps({
        'status': 'ok',
        'version': app.config['CURRENT_VERSION']
    }), status=200, content_type="application/json")

# @app.route('/threads')
# def threads():
#     # 获取当前运行中的线程数
#     num_threads = threading.active_count()
#     # 获取所有线程列表
#     threads = threading.enumerate()

#     # 创建一个空的线程列表
#     thread_list = []
#     # 遍历所有线程
#     for thread in threads:
#         # 获取线程名称
#         thread_name = thread.name
#         # 获取线程ID
#         thread_id = thread.ident
#         # 检查线程是否处于运行状态
#         is_alive = thread.is_alive()

#         # 将线程信息添加到线程列表中
#         thread_list.append({
#             'name': thread_name,
#             'id': thread_id,
#             'is_alive': is_alive
#         })

#     # 返回线程数和线程列表
#     return {
#         'thread_num': num_threads,
#         'threads': thread_list
#     }


@app.route('/db-pool-stat')
def pool_stat():
    # 获取数据库引擎

    engine = db.engine
    # 返回数据库连接池的状态信息
    return {
        'pool_size': engine.pool.size(),  # 连接池中的连接数
        'checked_in_connections': engine.pool.checkedin(),  # 已经签入到连接池但尚未使用的连接数
        'checked_out_connections': engine.pool.checkedout(),  # 已经签出使用的连接数
        'overflow_connections': engine.pool.overflow(),  # 当连接池数达到上限时，溢出到连接池的连接数
        'connection_timeout': engine.pool.timeout(),  # 连接超时时间
        'recycle_time': db.engine.pool._recycle  # 连接回收时间
    }

@app.route('/')
def index():
    return "hello world"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)