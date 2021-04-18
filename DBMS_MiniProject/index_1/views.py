from django.shortcuts import render,redirect,HttpResponse,Http404,HttpResponsePermanentRedirect
from .models import Customer
from django.db import connection
import cx_Oracle
import config as cfg
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def index(request):
    return render(request,"HTML/index.htm",{"c":Customer.objects.all()})

def sign_up(request):
    return render(request,'HTML/sign_up.htm')

def sign_up_logic(request):
    print("check")
    
    try:
        cursor = connection.cursor()
        if request.method == 'POST':
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            ph_no = request.POST['phone_no']
            x = 'c_id.nextval'
            cursor.execute("INSERT INTO CUSTOMER(c_id,Email,First_name,Last_name,phone_no) VALUES ("+x+",'"+email+"','"+f_name+"','"+l_name+"',"+str(ph_no)+")")
            connection.commit()
            return redirect('Home')
        else:
            return redirect('Home')
    except:
        return HttpResponse("<h1>Sorry for this type of error!!</h1><center><b style='font-size : 50px;'>Have you ever visited Pune's Shaniwarwada</b></center>")

def sign_in(request):
    return render(request,'HTML/signin.html')

def agencies_deal(request):
    if request.method == 'POST':
        city_name = 'Pune'
        conn = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
        cur = conn.cursor()
        myvar = cur.var(cx_Oracle.CURSOR)
        print(myvar)
        cur.callfunc('find_deals',myvar,[city_name])
        deals = myvar.getvalue().fetchall()
        print(deals[0])
        return render(request,'HTML/agencies.html',{'deals':deals[0][0]})

    
