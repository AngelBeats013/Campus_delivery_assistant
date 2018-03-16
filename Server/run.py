from app import app,db
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import User,Post
from app.views import postDone
import jpush as jpush
from config import app_key, master_secret
def jobfunction():
    print('Fresh Start')
    posts = Post.query.filter_by( status=2).all()
    for post in posts:

        handOverTimeStamp=post.handOverTimeStamp
        currentTime=time.time()#当前时间戳
        if(currentTime>handOverTimeStamp):
            if (post.status==0):
                post.status=5
                db.session.commit()
            if(post.status==1):
                post.status = 3
                postIntegral = post.postIntegral

                sender = User.query.filter_by(userName=post.senderName).first()
                receiver = User.query.filter_by(userName=post.receiverName).first()
                sender.sendPostNum += 1
                sender.integral -= postIntegral
                receiver.receivePostNum += 1
                receiver.goodEvaluation += 1
                receiver.integral += postIntegral * 1.5

                if receiver.integral < 0 or (receiver.evaluation < 0.3 and receiver.receivePostNum > 4):
                    receiver.grade = 0
                else:
                    if (receiver.integral < 100 and receiver.integral >= 0) or (
                            receiver.evaluation < 0.5 and receiver.receivePostNum > 4):
                        receiver.grade = 1
                    else:
                        if (receiver.integral >= 100 and receiver.integral < 500 and receiver.evaluation > 0.5):
                            receiver.grade = 2
                        if (receiver.integral >= 500 and receiver.integral < 1000 and receiver.evaluation > 0.6):
                            receiver.grade = 3
                        if (receiver.integral >= 1000 and receiver.integral < 3000 and receiver.evaluation > 0.7):
                            receiver.grade = 4
                        if (receiver.integral >= 3000 and receiver.evaluation > 0.8):
                            receiver.grade = 5
                db.session.commit()
                _jpush = jpush.JPush(app_key, master_secret)
                _jpush.set_logging("DEBUG")
                push = _jpush.create_push()
                alias = [post.receiverName]
                alias1 = {"alias": alias}
                push.audience = jpush.audience(
                    alias1
                )

                android = jpush.android(alert="订单:" + post.profile + "  " + post.place + " 发单人:" + post.senderName,
                                        title="你的订单已完成，评价：" + "Great")
                push.notification = jpush.notification(alert="Hello, JPush!", android=android)
                push.platform = jpush.all_
                print(push.payload)
                push.send()


if __name__ == '__main__':

      scheduler=BackgroundScheduler()
      scheduler.add_job(jobfunction,'cron',hour=23,minute=50)

      #scheduler.add_job(tick,'interval',seconds=3)
      scheduler.start()
      print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

      app.run()