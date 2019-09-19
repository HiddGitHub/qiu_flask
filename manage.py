# -*- coding:utf-8 -*-
import os
from apps import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

config_name = os.environ.get('FLASK_CONFIG') or 'default'
# config_name =  'default'
app = create_app(config_name)

manager = Manager(app)

manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()
