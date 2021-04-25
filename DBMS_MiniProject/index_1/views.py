from django.shortcuts import render,redirect,HttpResponse,Http404,HttpResponsePermanentRedirect
from django.contrib.auth.models import auth,User
from .models import Customer
from django.db import connection
from django.conf import settings
import cx_Oracle
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
global city_name,x,y,user

def index(request):
    return render(request,"HTML/index.htm")

def sign_up(request):
    return render(request,'HTML/sign_up.htm')

def sign_in(request):
    return render(request,'HTML/signin.html')


def sign_up_logic(request):
    # print("check")
    global user
    connection = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
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
            messages.success(request,"Successfully Signed Up!")
            return redirect('Home')
        else:
            messages.error(request,"Invalid Credentials , Please try again!")
            
            return redirect('Home')
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(error.message)
        if error.message == """ORA-20050: ERROR\nORA-06512: at "C##ADMIN.EMAIL_TRIG", line 7\nORA-04088: error during execution of trigger 'C##ADMIN.EMAIL_TRIG'""":
            return HttpResponse("<h1>Sorry for this type of error!!</h1><center><b style='font-size : 50px;'>PHONE NUMBER ALREADY EXISTS</b></center>")
        else:
            return HttpResponse("<h1>Sorry for this type of error!!</h1><center><b style='font-size : 50px;'>Have you ever visited Pune's Shaniwarwada</b></center>")



def sign_in_logic(request):

    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request,username = email,password = password)
            
            if user is not None:
                login(request,user)
                messages.success(request,"Successfully Signed In!")
                return redirect('Home')
            else:
                print('Home is not safe')
                return redirect('Home')
    except:
        return HttpResponse("Sorry But You didn't Logged in Rightly!!<center><b style='font-size : 50px;'>Have you ever visited Nashik's Kumbh Mela</b></center>")

@login_required(login_url='sign_in')
def sign_out_logic(request):
    try:
        if request.method == 'GET':
            logout(request)
            messages.success(request,"Successfully Signed Out!")
            return redirect('Home')
        else:
            return redirect('Home')
    except:
        return HttpResponse("Sorry But You didn't Logged in Rightly!!<center><b style='font-size : 50px;'>Have you ever visited Mumbai's Gateway Of India</b></center>")


@login_required(login_url='sign_in')
def agencies_deal(request):
    if request.method == 'POST':
        global city_name
        city_name = request.POST.get('term')
        print(city_name)
        conn = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
        cur = conn.cursor()
        myvar = cur.var(cx_Oracle.CURSOR)
        print(myvar)
        cur.callfunc('find_deals',myvar,[city_name])
        global deals
        deals = myvar.getvalue().fetchall()
        print(deals)
        return render(request,'HTML/agencies.html',{'deals':deals})


@login_required(login_url='sign_in')
def booking(request,agency,rating):
    global x,y,city_name
    x = agency
    y = rating
    connection = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
    cursor = connection.cursor()
    myvar = cursor.var(cx_Oracle.CURSOR)
    cursor.callproc('get_transport_charges',[x,city_name,myvar])
    charges = myvar.getvalue().fetchall()
    print(charges)
    return render(request,'HTML/AgencyPage.html',{'x':x,'y':y,'charges':charges})

@login_required(login_url='sign_in')
def send_email(request):
    global city_name,x,y,user
    connection = cx_Oracle.connect('c##admin','admin','localhost/orcl',encoding = 'UTF-8')
    cursor = connection.cursor()
    ph = cursor.callfunc('get_phone_number',str,[x,city_name])
    print(ph)
    if request.method == 'POST':
        user_ans = request.POST['term']
        passengers = request.POST['Passengers']
        a = request.user.first_name
        b = request.user.last_name
        c = request.user.email
        
        html_message = loader.render_to_string(
                                'HTML/mail_body.html',
                                {
                                    'a' : a,
                                    'b' : b,
                                    'user_ans' : user_ans,
                                    'city' : city_name,
                                    'x' : x,
                                    'y' : y,
                                    'details' : ph,
                                    'pass' : passengers,
                                }
                            )
        send_mail('BOOKING',None,settings.EMAIL_HOST_USER,[c],fail_silently=True,html_message=html_message)
        messages.success(request,"Mails have been sent on your mail !")
        return redirect('Home')



