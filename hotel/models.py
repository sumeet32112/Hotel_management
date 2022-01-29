from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import IntegerChoices
from django.db.models.fields import PositiveIntegerField



class Hotel(models.Model):
    hotelName=models.CharField(max_length=200)
    state=models.CharField(max_length=200,null=True,blank=False)
    totalRoom=models.IntegerField(null=True)
    image=models.ImageField(null=True,blank=True)
   

    def __str__(self):
        return self.hotelName

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url            

class Room(models.Model):
    name=models.ForeignKey(Hotel,on_delete=models.SET_NULL,null=True,blank=True)
    checkin_date=models.DateField(default=None,null=True)
    checkout_date=models.DateField(default=None,null=True)
    room_no=models.IntegerField(null=True)
    waiting=models.BooleanField(default=False)
    price=models.PositiveIntegerField(default=1,blank=False,null=False)
    # ROOM_TYPES = [
    #     ('Single-AC', 'Single-AC'),
    #     ('Double-AC', 'Double-AC'),
    #     ('Single-NON-AC', 'Single NON-AC'),
    #     ('Double-NON-AC', 'Double-NON-AC'),
    # ]
    # room_type=models.CharField(default='Single-AC',max_length=20, choices=ROOM_TYPES, null=False)
    
    def __str__(self):
        return  str(self.name.hotelName)+"_"+str(self.room_no) 

class Reservation(models.Model):
    checkin_date = models.DateField(default=None, null=True)
    checkout_date = models.DateField(default=None, null=True)
    
    user= models.ForeignKey(User,on_delete=models.DO_NOTHING, null=False, blank=False)			
    rooms_allocated = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
                                 
    def __str__(self):
        return f'{self.user.username} booked from {self.checkin_date} to {self.checkout_date}'
