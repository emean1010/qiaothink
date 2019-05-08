import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user

import json

import redis

cache = redis.StrictRedis()

from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u, result = User.register(form)
    print('result', result)
    return render_template("index.html", result=result)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))


def created_topic(user_id):
    # O(n)
    # ts = Topic.all(user_id=user_id)
    # return ts

    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    # O(k)+O(m*n)
    # rs = Reply.all(user_id=user_id)
    # ts = []
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     ts.append(t)
    # return ts
    #
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.one(id=r.topic_id)
            ts.append(t)

        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)

        return ts


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.setting'))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


@main.route('/user/<username>')
def user_detail(username):
    u = User.one(username=username)
    if u is None:
        abort(404)
    else:
        # 获取对应user的创建主题和回复主题
        creat_topics = order(Topic.all(user_id=u.id))
        reply_topics = get_reply_topics(u.id)
        return render_template('profile.html', user=u, creat_topics=creat_topics, reply_topics=reply_topics)


# 给主题按照创建日期排序，倒序
def order(ms):
    ms = sorted(ms, key=lambda m: m.created_time, reverse=True)
    return ms


# 获取回复对应的主题
def get_reply_topics(uid):
    reply_topics = []
    tids = []
    replies = order(Reply.all(user_id=uid))
    for r in replies:
        if r.topic_id not in tids:
            reply_topics.append(Topic.one(id=r.topic_id))
            tids.append(r.topic_id)
    return reply_topics


# 设置页面
@main.route('/setting')
def setting():
    u = current_user()
    return render_template('/setting.html', user=u)


# 修改用户名和签名
@main.route("/update", methods=['POST'])
def update():
    form = request.form.to_dict()
    u = current_user()
    User.update(u.id, username=form['name'])
    User.update(u.id, signature=form['signature'])
    return render_template('/setting.html', user=u)


# 修改用户密码，需要加盐
@main.route("/change_pass", methods=['POST'])
def change_pass():
    form = request.form.to_dict()
    u = current_user()
    if u.password == User.salted_password(form['old_pass']):
        User.update(u.id, password=User.salted_password(form['new_pass']))
    return render_template('/setting.html', user=u)