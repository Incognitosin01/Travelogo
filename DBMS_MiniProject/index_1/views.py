from django.shortcuts import render,redirect,HttpResponse,Http404,HttpResponsePermanentRedirect
from .models import Customer
from django.db import connection
# Create your views here.

global c_id
c_id=100


def index(request):
    return render(request,"HTML/index.htm",{"c":Customer.objects.all()})

def sign_up(request):
    return render(request,'HTML/sign_up.htm')

def sign_up_logic(request):
    print("check")
    global c_id
    cursor = connection.cursor()
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        ph_no = request.POST['phone_no']
        c_id = c_id+1
        cursor.execute("INSERT INTO CUSTOMER(email_id,customer_id,first_name,last_name,phone_no) VALUES ('"+email+"',"+str(150)+",'"+f_name+"','"+l_name+"',"+str(ph_no)+")")
        return redirect('Home')
    else:
        return redirect('Home')

    
