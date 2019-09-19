# -*- coding:utf-8 -*-


from flask import Blueprint,render_template,template_rendered,redirect

users_bp = Blueprint('users', __name__)
start_bp = Blueprint('start', __name__)


@users_bp.route("/1")
def  index1():

    return "hello world"

@start_bp.route('/')
def index():

    return render_template('users/index.html')
