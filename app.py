from flask import Flask
from models import *
from flask import render_template,redirect,url_for,request
from models import Student
from flask_sqlalchemy import SQLAlchemy
import config



from flask_session import Session
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
db = SQLAlchemy()

SECRET_KEY = "hsjwcf"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/flask_student?charset=utf8mb4" # 数据库连接URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/a")
def a():
    db.drop_all()
    db.create_all()
    return "aaa"
@app.route("/")
def index():
    datas = {
        "Student":Student.query.all()
    }
    print(datas)
    return render_template('index.html',**datas)

@app.route('/index1',endpoint="index1",methods=["POST","GET"])
def index1():
    if request.method == "POST":
        search = request.form.get("search")
        search_list = Student.query.filter(Student.name.like("%" + search + "%")).all()
        if search_list:

            return render_template("index.html", search_list=search_list)
        else:
            return render_template("index.html", errmsg = "该信息不存在")
    else:
        return render_template("index.html")

@app.route('/student_add/',endpoint="student_add",methods=["POST","GET"])
def student_add():
    if request.method == "POST":
        name = request.form.get("name")
        english = request.form.get("english")
        python = request.form.get("python")
        c = request.form.get("c")
        score = int(english) + int(python) + int(c)
        if name or english or python or c or score:
            add_data = Student(name=name,english=english,python=python,c=c,score=score)
            # print(name,auther,users,nowtime,fenlei)
            db.session.add(add_data)
            db.session.commit()
            return redirect(url_for('index1'))
        else:
            return render_template("add.html", errmsg = "添加失败")

    return render_template("add.html")


@app.route('/alter/<id>',endpoint="alter",methods=["POST","GET"])
def alter(id):
    if request.method == 'GET':
        print("id::", id)
        context = { "ids":id}
        return render_template('alter.html', **context)
    else:
        print("id::", id)
        name = request.form.get('name')
        english = request.form.get('english')
        python = request.form.get('python')
        c = request.form.get('c')
        score = int(english) + int(python) + int(c)
        a = Student.query.filter_by(id=id).first()
        a.name = name
        a.english = english
        a.python = python
        a.c = c
        a.score = score
        # db.session.add(a)
        db.session.commit()
        return redirect(url_for('index'))

# def alter(id):
#     l = request.args.get("l")
#     id1 = Student.query.filter_by(id=int(l)).all()
#     if request.method == "POST":
#         name = request.form.get("name")
#         english = request.form.get("english")
#         python = request.form.get("python")
#         c = request.form.get("c")
#         score = int(english) + int(python) + int(c)
#         if name and english and python and c and score:
#             if id1:
#                 Student.query.filter_by(id=int(l)).update({"name":name,"english":english,"python":python,"c":c,"score":score})
#                 db.session.commit()
#                 return render_template("index.html")
#             else:
#                 context = {"all": id1, "errmsg": "修改失败"}
#                 return render_template("index.html", **context)
#                 # return render_template('index.html', errmsg='*请填写完整')
#         else:
#             context = {"all": id1,"errmsg":"信息输入不完整"}
#             print(context)
#             return render_template("index.html", **context)
#     context = {"all":id1}
#     return render_template("index.html", **context)

# @app.route("/aaa",methods = ["GET","POST"])
# def aaa():
#     return render_template("index.html")

@app.route('/delete/<id>', methods=['GET'])
def delete(id):

    students = Student.query.filter_by(id=id).first()
    db.session.delete(students)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    # db.create_all()
    # # db.init_app(app)
    app.run()
