from django.shortcuts import render,redirect,HttpResponse,Http404,HttpResponsePermanentRedirect
from django.contrib.auth.models import auth,User
from .models import Customer
from django.db import connection
import cx_Oracle
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def index(request):
    return render(request,"HTML/index.htm")

def sign_up(request):
    return render(request,'HTML/sign_up.htm')

def sign_in(request):
    return render(request,'HTML/signin.html')


def sign_up_logic(request):
    # print("check")
    
    try:
        cursor = connection.cursor()
        if request.method == 'POST':
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            ph_no = request.POST['phone_no']
            password = request.POST['password']
            x = 'c_id.nextval'
            cursor.execute("INSERT INTO CUSTOMER(c_id,Email,First_name,Last_name,phone_no,password) VALUES ("+x+",'"+email+"','"+f_name+"','"+l_name+"',"+str(ph_no)+",'"+password+"')")
            connection.commit()
            user = User.objects.create_user(username = email,first_name = f_name,last_name = l_name,email = email,password = password)
            user.save()
            return redirect('Home')
        else:
            return redirect('Home')
    except:
        return HttpResponse("<h1>Sorry for this type of error!!</h1><center><b style='font-size : 50px;'>Have you ever visited Pune's Shaniwarwada</b></center>")


def sign_in_logic(request):

    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request,username = email,password = password)
            
            if user is not None:
                login(request,user)
                return redirect('Home')
            else:
                print('Home is not safe')
                return redirect('Home')
    except:
        return HttpResponse("Sorry But You didn't Logged in Rightly!!<center><b style='font-size : 50px;'>Have you ever visited Nashik's Kumbh Mela</b></center>")

def sign_out_logic(request):
    try:
        if request.method == 'GET':
            logout(request)
            return redirect('Home')
        else:
            return redirect('Home')
    except:
        return HttpResponse("Sorry But You didn't Logged in Rightly!!<center><b style='font-size : 50px;'>Have you ever visited Mumbai's Gateway Of India</b></center>")


@login_required(login_url='sign_in')
def agencies_deal(request):
    if request.method == 'POST':
        city_name = request.POST.get('term')
        print(city_name)
        conn = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
        cur = conn.cursor()
        myvar = cur.var(cx_Oracle.CURSOR)
        print(myvar)
        cur.callfunc('find_deals',myvar,[city_name])
        deals = myvar.getvalue().fetchall()
        print(deals)
        return render(request,'HTML/agencies.html',{'deals':deals})

    
