Flask 搭建博客  
![](https://img.shields.io/badge/python-3.6-orange.svg) ![](https://img.shields.io/badge/Flask-0.12-orange.svg)
===
环境
-----
* Python:3.6.1
* Flask:0.12.1

功能
----
* 注册、登录、登出
* 更改/重置密码
* 注册用户文章留言
* 管理员markdown文章编辑，代码高亮
* 文章分享
* 利用QQ音乐API实现简单音乐播放器功能
* 基于阅读量的阅读排行，最新评论

下载
----
```Bash
git clone git@github.com:Shuangtonglee/flask-blog.git
```
配置
----
　按需求修改config.py。隐私信息采用设置环境变量的方法获得。设置管理员邮箱，然后用管理员邮箱注册即可成管理员。

安装
----
```Bash
pip install -r requirements #安装依赖
pip manage.py db upgrade #创建数据库
python manage.py runserver #运行，浏览器中打开http://127.0.0.1:5000/
```
TODO
----
* 移动端适配
* 文章编辑界面优化
