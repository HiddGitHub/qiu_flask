# -*- coding:utf-8 -*-
from  flask import Flask

from apps.config import config

from apps.view import config_blueprint
def create_app(config_name):
    # 创建app实例对象
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config.get(config_name) or 'default')

    # 执行额外的初始化
    config.get(config_name).init_app(app)

    # 配置蓝本
    config_blueprint(app)

    return app
