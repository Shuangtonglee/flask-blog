#若该函数在home.py 中，在my_view 中from home import send_email,运行时home.py 中先import my_view
#,然后在my_view 中from home import send_email，但是在home 中 import view 还没有完成，所以app.register_blueprint(my_view.views) 导入不成功
#应该算是循环导入问题
from flask_mail import Message
from flask import render_template,current_app
from threading import  Thread
from . import mail




def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX']+''+subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr