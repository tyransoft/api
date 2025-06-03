from django.db import models
from django.contrib.auth.models import User
from .utils import haversine
from  django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
import secrets

class Plan(models.Model):
    DURATION_CHOICES = [
        ('weekly','اسبوعي'),
        ('monthly', 'شهري'),
        ('quarterly', 'ربع سنوي'),
        ('halfly', 'نصف سنوي'),    
        ('yearly', 'سنوي'),
    ]

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    description=models.TextField()
    def __str__(self):
        return self.name

class Customers(models.Model):
    status={
        ('available','available'),
        ('onride','onride')
    }
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_index=True)
    phone = models.CharField(max_length=20)
    image=models.ImageField(upload_to='customer_images/',null=True)
    gender=models.CharField(max_length=25)
    born_date=models.DateTimeField()
    status=models.CharField(max_length=30,choices=status,db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    joined_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name




class Drivers(models.Model):
    status={
        ('available','available'),
        ('driveing','driveing')
    }
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_index=True)
    phone = models.CharField(max_length=20)
    car_image=models.ImageField(upload_to='car_images/',null=True)
    license_image=models.ImageField(upload_to='license_images/',null=True)
    profile_image=models.ImageField(upload_to='profile_images/',null=True)
    proof_image=models.ImageField(upload_to='proof_images/',null=True)

    gender=models.CharField(max_length=20)

    license_id=models.CharField(max_length=20)
    national_number=models.CharField(max_length=30)
  
    car_type=models.CharField(max_length=30,db_index=True)
    car_id=models.CharField(max_length=20)
  
    born_date=models.DateTimeField()
    status=models.CharField(max_length=30,choices=status,db_index=True)
  
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    pocket = models.IntegerField(default=0)

    joined_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
    

class Transaction(models.Model):
    status={
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),

    }
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE,db_index=True)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,null=True,db_index=True)
    latitude_of_drop = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude_of_drop = models.DecimalField(max_digits=9, decimal_places=6)
    car_type=models.CharField(max_length=30,db_index=True)
    status=models.CharField(max_length=50,choices=status,db_index=True)
    description=models.TextField()
    weight=models.FloatField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  

    distance=models.DecimalField(max_digits=9, decimal_places=6,null=True)    
    
    shorter_distance=models.DecimalField(max_digits=9, decimal_places=6,null=True)
    
    
    started_at=models.DateTimeField(blank=True,null=True)
    ended_at=models.DateTimeField(blank=True,null=True)

    time=models.FloatField(blank=True,null=True)

    ride_added_date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.driver.user.first_name if self.driver else None}/{self.customer.user.first_name}'
    
    def save(self,*args,**kwargs):
        
        cus_lat, cus_long = self.customer.latitude, self.customer.longitude
        
        if self.driver:
            dri_lat, dri_long = self.driver.latitude, self.driver.longitude

            if cus_lat and cus_long and self.latitude_of_drop and self.longitude_of_drop:
                self.distance = haversine(cus_lat, cus_long, self.latitude_of_drop, self.longitude_of_drop)

            if cus_lat and cus_long and dri_lat and dri_long:
                self.shorter_distance = haversine(cus_lat, cus_long, dri_lat, dri_long)
        else:
            if cus_lat and cus_long and self.latitude_of_drop and self.longitude_of_drop:
                self.distance = haversine(cus_lat, cus_long, self.latitude_of_drop, self.longitude_of_drop)
        

        super().save(*args, **kwargs)



class DriversReview(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE,db_index=True)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,related_name='driver_rating',db_index=True)
    Transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,db_index=True)
    comment=models.TextField()
    review=models.IntegerField(choices=[(i, i) for i in range(1,6)])
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'review from {self.customer.user.first_name} to {self.driver.user.first_name}'

class CutomersReview(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE ,related_name='customer_ratings',db_index=True)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,db_index=True)
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,db_index=True)
    comment=models.TextField()
    review=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'review from {self.driver.user.first_name} to {self.customer.user.first_name}'



class Proposal(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE,db_index=True)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,db_index=True)
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,db_index=True)
    price=models.FloatField()
    comment=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'driver:{self.driver.user.first_name}/customer{self.customer.user.first_name}-{self.date}'
    
class Cards(models.Model):
    code=models.CharField(max_length=13,db_index=True,unique=True)
    value=models.IntegerField(db_index=True)
    is_used=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.code}-{self.value}د.ل//{self.is_used}'
    @staticmethod
    def generate_card_number():
        while True:
            number=''.join([str(secrets.randbelow(10)) for _ in range(13)])
            if len(set(number)):
                if not Cards.objects.filter(code=number).exists():
                    return number
    @staticmethod            
    def generate_cards(number_of_cards,value):
        generated_cards=[]
        for _ in range(number_of_cards):
            code=Cards.generate_card_number()
            card=Cards(code=code,value=value)
            card.save()
            generated_cards.append(card)
        return generated_cards     


class Subscription(models.Model):
    driver = models.ForeignKey(Drivers, on_delete=models.CASCADE)  
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)  
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)  
    is_active = models.BooleanField(default=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # السعر النهائي بعد الخصم
    
    def save(self, *args, **kwargs):
        self.final_price = self.plan.price
        
       
        
        if not self.start_date:
            self.start_date = timezone.now().date()
            
        if self.plan.duration == 'monthly':
            self.end_date = self.start_date + timedelta(days=30)  
        elif self.plan.duration == 'quarterly':
            self.end_date = self.start_date + timedelta(days=90)  
        elif self.plan.duration == 'yearly':
            self.end_date = self.start_date + timedelta(days=365)  
        elif self.plan.duration == 'halfly':
            self.end_date = self.start_date + timedelta(days=180)  

        elif self.plan.duration == 'weekly':
    
            self.end_date = self.start_date + timedelta(days=7)
        
             
        if not self.end_date:
            self.end_date = self.start_date     


       
            
        super().save(*args, **kwargs)

    def remaining_days(self):
        if self.end_date:
            remaining = self.end_date - timezone.now().date()
            return remaining.days
        return 0
    def __str__(self):
        return f"Subscription for {self.driver.user.first_name} to {self.plan.name}"
