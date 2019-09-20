# -*- coding:utf-8 -*-
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
# 创建对象
bootstrap = Bootstrap()
# 初始化
def config_extensions(app):
    bootstrap.init_app(app)
    # bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
