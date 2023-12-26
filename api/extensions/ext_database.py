from flask_sqlalchemy import SQLAlchemy  # 导入Flask_SQLAlchemy模块中的SQLAlchemy类

db = SQLAlchemy()  # 创建SQLAlchemy实例对象db

def init_app(app):
    """
    初始化应用程序。

    参数:
    app: Flask应用程序对象。
    """
    db.init_app(app)