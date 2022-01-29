from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse,HttpResponseRedirect, request
import datetime
from django.contrib import messages
from .forms import *
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import razorpay
from hotel_management.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))


def user_login(request):
    data={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect('/')
        else:
           data['error']="username or password is incorrect"
           res=render(request,'hotel/login.html',data)
           return res
    else:
        return render(request,'hotel/login.html',data)

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save() 
            login(request,user)
            messages.success(request,"registration is successful..")
            return redirect('user_login/')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request,"hotel/signup.html",{"register_form":form})  



def home(request):
    form=search()
    hotels=Hotel.objects.all()   
    context={'hotels':hotels,'form':form,'user':request.user}
    return render(request,'hotel/home.html',context)

@login_required(login_url="user_login")
def user_profile(request):
    user=request.user
    bookings=Reservation.objects.filter(user=user)
    context={'user':user,'bookings':bookings}
    return render(request,'hotel/user_profile.html',context)

@login_required(login_url="user_login")
def search_hotel(request):
    if request.method =="POST":
        form=search(request.POST)
        if form.is_valid():
            checkin=form.cleaned_data['checkin']
            checkout=form.cleaned_data['checkout']
            state=form.cleaned_data['state']
            #room_type=form.cleaned_data['room_type']
            if checkin > checkout or checkin < datetime.date.today():
                messages.warning(request,'please enter the proper dates')
                return redirect('home')
            hotels=Hotel.objects.filter(state=state)    
            values={}
            for hotel in hotels:
                rooms=Room.objects.filter(name=hotel)
                cnt=0
                for room in rooms:
                    if room.checkin_date>checkout or room.checkout_date<checkin:
                         cnt+=1
                         values[hotel]=cnt
            context={'values':values,'checkin':checkin,'checkout':checkout}
            return render(request,'hotel/search_hotel.html',context)
        else:
            messages.warning(request, 'Requested Page Not Found')
            return redirect('home')

def hotel_info(request,hotel_id):
    form=search()
    hotel=Hotel.objects.get(id=hotel_id)
    context={'hotel':hotel,'form':form}
    return render(request,'hotel/hotel_info.html',context) 

@login_required(login_url="user_login")
def book_room(request,hotel_id,checkin,checkout):
    hotel=Hotel.objects.get(id=hotel_id)
    rooms=Room.objects.filter(name=hotel)
    values=[]
    for room in rooms:
        if str(room.checkin_date)>checkout or str(room.checkout_date)<checkin:
            values+=[room]
    context={'hotel':hotel,'values':values,'checkin':checkin,'checkout':checkout}
    return render(request,'hotel/book_room.html',context) 

@login_required(login_url="user_login")
def cancel(request,id):
    reservation=Reservation.objects.get(id=id)
    reservation.delete()
    return redirect('user_profile') 
     

@login_required(login_url="user_login")
def reservation_room(request,room_id,checkin,checkout):
     room=Room.objects.get(id=room_id)
     amount=(room.price)*100
     currency="INR"
     payment_order=client.order.create(dict(amount=amount,currency=currency,payment_capture=1))
     context={}
     payment_order_id=payment_order['id']
     context={'room':room,'checkin':checkin,'checkout':checkout,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id}
     return render(request,'hotel/reservation.html',context)                    
                        
@login_required(login_url="user_login")
@csrf_exempt 
def process_booking(request,room_id,checkin,checkout):
        
        room=Room.objects.get(id=room_id)
        room.checkin_date=checkin
        room.checkout_date=checkout
        room.waiting=True
        room.save()

        Reservation.objects.create(
            checkin_date=checkin,
            checkout_date=checkout,
            user=request.user,
            rooms_allocated=room,
        )
        return HttpResponse("payment is successfull.....your room has been booked ")


