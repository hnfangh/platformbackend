from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # 解决前端后端跨域访问问题
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@47.106.133.253/python'
api = Api(app)
db = SQLAlchemy(app)


# 数据库用户信息表ORM
class User(db.Model):

    __tablename__ = 'user_python'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# 测试用例数据库的ORM
class TestCase(db.Model):

    # 定义表名字
    __tablename__ = 'testcase_python'

    # 定义表字段and属性
    # id为int类型，且是主键
    id = db.Column(db.Integer, primary_key=True)
    # name/desc/data为string类型，且唯一主键，不能为空
    name = db.Column(db.String(200), unique=True, nullable=False)
    desc = db.Column(db.String(200), unique=True, nullable=False)
    data = db.Column(db.String(500), unique=True, nullable=False)

    # # 设置外键关联
    # uid = db.Column(db.Integer, db.ForeignKey('user_python.id'),nullable=False)
    #
    # # 确定关联关系
    # user = db.relationship('User', backref=db.backref('testcase', layz=True))

    # 显示属性
    def __repr__(self):
        return '<TestCase %r>' % self.name

# 登陆管理
class Login(Resource):

    def get(self):
        return {'date':'get info data'}

    def post(self):
        app.logger.info(request.json)
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username,password=password).first()

        if user is None:
            return {
                'data':None,
                'errorcode':1
            }
        else:
            return {
                'data':{
                    "id":user.id,
                    "username": username
                },
                'errorcode':0
            }

# 测试用例管理
class TestCaseResource(Resource):

    # 查询用例
    def get(self):
        # 查询数据库中所有的数据
        testcase = TestCase.query.all()
        app.logger.info(testcase)
        res = [{
            'id':t.id,
            'name':t.name,
            'desc':t.desc,
            'data':t.data
        } for t in testcase]

        return {
            'data':res,
            'errorcode':0
        }

    # 新增用例
    def post(self):
        app.logger.info(request.json)
        # 从前端请求输入参数传入后端DB新增
        testcase = TestCase(name=request.json['name'],desc=request.json['desc'],data=request.json['data'])
        # 写入到数据库中
        db.session.add(testcase)
        db.session.commit()
        db.session.close()
        return {
            'data':'ok',
            'error': 0,
            'msg': '用例新增成功'
        }

    # 更新用例
    def put(self):
        app.logger.info(request.json)
        # 修改前查询
        testcase = TestCase.query.filter_by(id=request.json['id']).first()
        testcase.name = request.json['name']
        testcase.desc = request.json['desc']
        testcase.data = request.json['data']
        # 更新操作
        db.session.flush()
        db.session.commit()
        # 修改后查询
        testcase2 = TestCase.query.filter_by(id=request.json['id']).first()
        app.logger.info(testcase2)
        db.session.close()
        return {
            'data':'ok',
            'error':0,
            'msg':'用例修改成功'
        }

    # 删除用例
    def delete(self):
        app.logger.info(request.json)
        # 查询对应ID的用例数据
        testcase = TestCase.query.filter_by(id=request.json['id']).first()
        print(testcase)
        db.session.remove(testcase)
        db.session.commit()
        db.session.close()
        return {
            'data': 'ok',
            'error': 0,
            'msg': '用例删除成功'
        }



api.add_resource(Login,'/login')
api.add_resource(TestCaseResource,'/testcase')





if __name__ == '__main__':
    # db.create_all()  创建表和数据
    app.run(debug=True)