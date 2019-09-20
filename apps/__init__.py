# -*- coding:utf-8 -*-
from  flask import Flask
from flask import Flask, render_template
from apps.config import config
from  apps.extensions import config_extensions
from apps.view import config_blueprint


def config_errorhandler(app):
    # 如果在蓝本定制，则只针对蓝本的错误有效。
    # 可以使用app_errorhandler定制全局有效的错误显示
    # 定制全局404错误页面
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html',e=e)




def create_app(config_name):
    # 创建app实例对象
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config.get(config_name) or 'default')

    # 执行额外的初始化
    config.get(config_name).init_app(app)

    # 配置蓝本
    config_blueprint(app)

    # 加载扩展
    config_extensions(app)

    # 配置全局错误处理
    config_errorhandler(app)

    return app
