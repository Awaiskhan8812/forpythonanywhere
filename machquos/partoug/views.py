from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect


# Create your views here.

def house(request):
    'show home page'
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('txt1_username')
        password = request.POST.get('txt1_password')
        phone = request.POST.get('txt1_username')
        Gender = request.POST.get('gender1')
        dob = request.POST.get('txt_dob1')
        try:
            cursor = connection.cursor()
            sql = 'insert into awais2 values(null, %s,%s,%s,%s,%s)'
            val = (username ,password , phone , Gender , dob)
            cursor.execute(sql, val)
            success = ''
            fail = ""
            id = cursor.lastrowid
            if id:
                success = "registraction success"
            else:
                fail = "registraction fail"
            return render(request , 'register.html' ,{'success': success,'fail':fail})
        except Exception as e:
            return render(request , 'register.html' , {'fail': str(e)})
    else:
        return render (request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        cursor=connection.cursor()
        user = request.session['user']

        sql="select * from awais2 where username = %s and password = %s "
        val = (username , password)
        cursor.execute(sql,val)
        record = cursor.fetchall()
        if record:
            request.session['user'] = record[0][1]
            request.session['user_id'] = record[0][0]
            request.session['pasword'] = record[0][2]
            return render (request,'saving.html',{'user': user ,'password': password})
        else:
            return render (request,'login.html',{'message':'invalid username or password'})
    else:
        return render(request,'login.html')

def todo(request):
    if not request.session.get('user'):
        return redirect('/partoug/login')
    user_id = request.session['user_id']
    user = request.session['user']
    sql = "select * from save2 where user_id =%s"
    val = [str(user_id)]
    cursor = connection.cursor()
    cursor.execute(sql,val)
    records = cursor.fetchall()
    return render(request, 'todo.html', {'user': user, 'save2':records})

def save(request):
    title = request.POST.get('txt_title')
    content = request.POST.get('txt_description')
    user_id = request.session['user_id']
    cursor = connection.cursor()
    sql = "insert into save2 values (null, %s, %s, %s)"
    val = (title , content,str(user_id ))
    cursor.execute(sql,val)
    return redirect ('/partoug/todo')

def delete(request):
    id = request.GET.get('id')
    cursor = connection.cursor()
    sql = "delete from save2 where todo_id = %s"
    val = (str(id))
    cursor.execute(sql,val)
    return redirect('/partoug/todo')

def saving(request):
    if not request.session.get('user'):
        return redirect('/partoug/login')
    username = request.POST.get('txt_username')
    password = request.POST.get('txt_password')
    gender = request.POST.get('gender')
    phone = request.POST.get('txt_phone')
    date = request.POST.get('txt_date')
    cursor = connection.cursor()
    sql = "insert into awais3 values (null,%s,%s,%s,%s,%s)"
    val = (username , password , gender , phone , date)
    cursor.execute(sql,val)
    return redirect(request, '/partoug/saving')

def insert(request):
    username = request.POST.get('txt_username')
    password = request.POST.get('txt_password')
    gender = request.POST.get('gender')
    phone = request.POST.get('txt_phone')
    date = request.POST.get('txt_date')
    cursor = connection.cursor()
    sql = "insert into awais3 values (null, %s, %s, %s ,%s , %s)"
    val = (username , password , gender , phone , date)
    cursor.execute(sql,val)
    return redirect ('/partoug/saving')

def logout(request):
    request.session.clear()
    return redirect('/todo')