# -*- coding:utf-8 -*-

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint,render_template,template_rendered,redirect
from flask import request,session,url_for,g,flash
from apps.extensions import db
from apps.model import User
from apps.email import send_mail
from sqlalchemy import or_
from flask_login import login_user, logout_user, current_user
from apps.forms.users import RegisterForm, LoginForm, UserPasswordForm, EmailForm, EUForm, AuthCodeForm, \
    ResetPwdForm #CommentForm ,

users_bp = Blueprint('users', __name__)
# start_bp = Blueprint('start', __name__)


@users_bp.route('/register', methods=('GET', 'POST'))
def register():
    form  = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        # 发激活邮件
        # 生成一个token，令牌，包含失效，包含用户信息()
        token = user.generate_activate_token()
        send_mail([user.email], '激活邮件', 'email/activate', username=user.username, token=token)
        flash('注册成功')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter(or_(User.username == username, User.email == username)).first()
        if not user:
            flash('用户名或密码错误')
        elif not user.confirm:
            flash('用户未被激活,请先激活在登录')
        elif not user.verify_password(form.password.data):
            flash('用户名或密码错误')
        else:
            login_user(user, remember=form.remember.data)
            flash('登录成功')
            return 'hello '+username
    return render_template('users/login.html', form=form)


@users_bp.route('/logout/')
def logout():
    logout_user()
    return render_template('users/login.html')


@users_bp.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    form = UserPasswordForm()
    if form.validate_on_submit():
        newpwd = form.newpwd.data
        user = current_user._get_current_object()
        user.password = newpwd
        db.session.add(user)
        # 退出登录
        logout_user()
        flash('密码修改成功，请重新登录')
        return redirect(url_for('users.login'))
    return render_template('users/change_password.html', form=form)


@users_bp.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():
    form1 = EUForm()
    global authcode
    authcode = random_string(length=6)
    if form1.validate_on_submit():
        global Uname
        username = form1.username.data
        Uname = username
        user = User.query.filter(or_(User.username == username, User.email == username)).first()
        # print(user.email)
        if user:
            send_mail([user.email], '验证码邮件', 'email/authcode', username=user.username, authcode=authcode)
            flash('验证码邮件已发送,注意查收')
            return redirect(url_for('users.reset_password2'))
        else:
            flash('请输入正确的用户名或邮箱')
    return render_template('users/reset_password.html', form1=form1)

# 生成随机的字符串
def random_string(length=32):
    import random
    import string
    base_str = string.ascii_letters + string.digits
    return ''.join(random.choice(base_str) for _ in range(length))

# 修改邮箱
@users_bp.route('/change_email/', methods=['GET', 'POST'])
def change_email():
    form = EmailForm()
    if form.validate_on_submit():
        newemail = form.email.data
        infoDict = {'user_id': current_user.id, 'newemail': newemail}
        token = User.generate_token(infoDict)
        send_mail([newemail], '修改邮箱邮件', 'email/change_email', username=current_user.username, token=token)
        flash('邮件已发送，注意查收')
        form.email.data = ''
    return render_template('users/change_email.html', form=form)

@users_bp.route('/success_change_email/<token>/')
def success_change_email(token):
    data = User.check_token(token)
    if data:
        user = User.query.get(data['user_id'])
        if user.email != data['newemail']:
            user.email = data['newemail']
            db.session.add(user)
        flash('邮箱修改成功,请查看个人信息')
        # return redirect(url_for('main.pzl'))
        return redirect(url_for('users.login'))
    else:
        flash('邮件已失效,请重新发送')
        return redirect(url_for('users.change_email'))

