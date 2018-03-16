import os

CSRF_ENABLED = True #跨站请求攻击保护
SECRET_KEY = 'you-will-never-guess'#设置当CSRF启用时有效，这将生成一个加密的token供表单验证使用，你要确保这个KEY足够复杂不会被简单推测

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')#这是我们的数据库文件的路径。
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')#是用来存储迁移数据库文件的文件夹。

app_key = u'1e0aff83c82a4ad9c860474f'
master_secret = u'4d282cdb7c9b8a40391d08df'