# -*- coding:utf-8 -*-

from .users import users_bp


#实例化蓝图

DEFAULT_BLUEPRINT = (


    (users_bp,'/users'),
    # (start_bp,'/'),

)


# 封装配置蓝本的函数
def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
