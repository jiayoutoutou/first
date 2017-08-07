from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
import pymysql
import json
from utils import sqlhelper
from app01 import models

def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pwd=request.POST.get("password")
        ret=models.User_infor.objects.filter(name=username,pwd=pwd).first()
        # obj=sqlhelper.SqlHelper()
        # ret=obj.get_one("select username from user_infor where username=%s and password=%s",[username,pwd,])
        if ret:
            obj=redirect("/teacher.html")
            obj.set_cookie("ticket",ret.name)
            return obj
    return render(request, 'login.html')

def auth(func):
    def wrapper(request):
        username = request.COOKIES.get("ticket")
        if not username:
            return redirect("/login/")
        return func(request,username)
    return wrapper

@auth
def teacher(request,username):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("""select teacher.id,teacher.name,class.title from teacher LEFT JOIN tea_cla on teacher.id=tea_cla.teacher_id 
              left join class on class.id=tea_cla.class_id""")
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    teacher_list={}
    for row in ret:
        if row["id"] in teacher_list:
            teacher_list[row["id"]]["titles"].append(row["title"])
        else:
            teacher_list[row["id"]]={"id":row["id"],"name":row["name"],"titles":[row["title"],]}
    return render(request, "teacher.html", {"teacher_list": teacher_list.values(), "username":username})
def model_modify(request):
    # {"name":$name, "class_id_list":$class_id_list,"operate":$operate,"teacher_id":$id}
    ret={"status":True,"message":None}
    name=request.POST.get("name")
    class_list_id=request.POST.getlist("class_list_id")
    operate=request.POST.get("operate")
    if len(name.strip())==0 or len(class_list_id)==0:
        ret["status"]=False
        ret["message"]="教师姓名和课程不能为空"
    else:
        try:
            if operate=="add":
                teacher_id=sqlhelper.modify("insert into teacher(name) values(%s)",name)
                for i in class_list_id:
                    sqlhelper.modify("insert into tea_cla(teacher_id,class_id) values(%s,%s)",teacher_id,i)
            else:
                obj = sqlhelper.SqlHelper()
                teacher_id = request.POST.get('teacher_id')
                obj.modify("delete from tea_cla where teacher_id=%s", [teacher_id,])
                if operate=="edite":
                    obj.multiple_modify("insert into tea_cla(teacher_id,class_id) values(%s,%s)",[(teacher_id,i) for i in class_list_id])
                    obj.modify("update teacher set name=%s where id=%s ",[name,teacher_id,])
                else:
                    obj.modify("delete from teacher where id=%s",[teacher_id,])
        except Exception as e:
            ret["status"] = False
            ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))
def model_message(request):
    obj=sqlhelper.SqlHelper()
    operate=request.POST.get("operate")
    ret = obj.get_list("select id,title from class", [])
    class_id_list=[]
    if operate=="add":
        return HttpResponse(json.dumps([ret,class_id_list]))
    else:
        teacher_id=request.POST.get("teacher_id")
        class_id=obj.get_list("select class_id from tea_cla where teacher_id=%s",[teacher_id,])
        class_id_list=[i["class_id"] for i in class_id]
        return HttpResponse(json.dumps([ret, class_id_list]))

@auth
def search_class(request,username):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo',charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    ret=cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, "class.html", {"class_list":ret, "username":username})
def add_class(request):
    if request.method=="GET":
        return render(request,"add_class.html")
    else:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo',charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        title=request.POST.get("title")
        cursor.execute("insert into class(title) values(%s)",title)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/search_class/")
def del_class(request):
    num=request.GET.get("id")
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo',charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [num,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/search_class/")
def edite_class(request):
    num=request.GET.get("id")
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method=="GET":
        cursor.execute("select id,title from class where id=%s",num)
        ret=cursor.fetchone()
        print(ret,11111111111111111111111111111111111111111111)
        cursor.close()
        conn.close()
        return render(request,"edite_class.html",{"ret":ret})
    else:
        title=request.POST.get("title")
        cursor.execute("update class set title=%s where id=%s", [title,num,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/search_class/')

@auth
def student(request,username):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='152131', db='Djingo', charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select student.id,student.name,student.class_id,class.title from student left join class on student.class_id=class.id")
    ret = cursor.fetchall()
    cursor.execute("select id,title from class")
    ret2 = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, "student.html", {"student_list":ret, "class_list":ret2, "username":username})
def model_modify_student(request):
    title = request.POST.get("title")
    class_id=request.POST.get("class_id")
    student_id=request.POST.get("student_id")
    operate=request.POST.get("operate")
    if len(title) == 0:
        return HttpResponse("error")
    else:
        if operate=="add":
            sqlhelper.modify("insert into student(name,class_id) values(%s,%s)", title,class_id)
        elif operate=="edite":
            sqlhelper.modify("update student set name=%s,class_id=%s where id=%s", title, class_id, student_id)
        else:
            sqlhelper.modify("delete from student where id=%s", student_id)
        return HttpResponse("ok")

