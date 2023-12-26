import redis
from redis.connection import SSLConnection, Connection
# 初始化Redis客户端
redis_client = redis.Redis()

def init_app(app):

    # 根据配置决定使用哪种连接类
    connection_class = Connection
    if app.config.get('REDIS_USE_SSL', False):
        connection_class = SSLConnection

    # 配置Redis连接池参数
    redis_client.connection_pool = redis.ConnectionPool(**{
        'host': app.config.get('REDIS_HOST', 'localhost'),  # Redis服务器主机地址
        'port': app.config.get('REDIS_PORT', 6379),  # Redis服务器端口号
        'username': app.config.get('REDIS_USERNAME', 'admin'),  # Redis服务器用户名
        'password': app.config.get('REDIS_PASSWORD', 'bb123456'),  # Redis服务器密码
        'db': app.config.get('REDIS_DB', 0),  # Redis数据库索引
        'encoding': 'utf-8',  # 连接编码方式
        'encoding_errors': 'strict',  # 编码错误处理方式
        'decode_responses': False  # 响应解码开关
    }, connection_class=connection_class)

    # 将Redis客户端对象添加到app的extensions字典中
    app.extensions['redis'] = redis_client
