# QiaoThink
基于 Flask 实现的个人论坛

## 部署
+ 代码仓库：https://github.com/emean1010/qiaothink
+ 论坛网址：http://qiaothink.com
+ 首页提供测试账号登录：
    + 账号：abc
    + 密码：123

## 使用
[![](https://img.shields.io/badge/Flask-1.0.2-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Jinja-2.10-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/SQLAlchemy-1.3.2-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Celery-4.3.0-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Redis-5.0.4-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Supervisor-4.0.2-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Nginx-1.16.0-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/Gunicorn-19.9.0-green.svg)](https://github.com/emean1010/qiaothink)
[![](https://img.shields.io/badge/QiaoThink-个人论坛-orange.svg)](https://github.com/emean1010/qiaothink)

## 注册/登录 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/login.gif)
账户名有限制，注册失败有提示

## 文章分区/创建话题/删除话题 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/post.gif)
支持markdown格式
权限限制，只能删除自己创建的话题

## 回复评论 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/reply.gif)
支持markdown格式

## 发送邮件/邮件通知 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/send.gif)
邮件会显示在双方的消息页面，邮件能发送至对方邮箱

## 评论 @ 功能/消息通知 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/AT.gif)
AT 内容会显示在双方的消息页面

## 个人设置 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/setting.gif)
用户可以设置自己的头像/签名/密码

## 用户近期动态/查看他人动态 ##
![](https://github.com/emean1010/qiaothink/blob/master/gif/profile.gif)
创建话题和参与话题分别按照创建时间、回复时间排序
