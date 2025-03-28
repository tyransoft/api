from django.db import models
from django.contrib.auth.models import User
from .utils import haversine
from  django.utils.timezone import now

class Customers(models.Model):
    status={
        ('available','available'),
        ('onride','onride')
    }
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    image=models.ImageField(upload_to='customer_images/',null=True)
    status=models.CharField(max_length=30,choices=status)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    joined_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name




class Drivers(models.Model):
    status={
        ('available','available'),
        ('driveing','driveing')
    }
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    image=models.ImageField(upload_to='car_images/',null=True)
    license_image=models.ImageField(upload_to='license_images/',null=True)
    license_id=models.CharField(max_length=20)
    national_number=models.CharField(max_length=30)
  
    car_type=models.CharField(max_length=30)
    car_id=models.CharField(max_length=20)
  
    born_date=models.DateTimeField()
    status=models.CharField(max_length=30,choices=status)
  
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed=models.FloatField(null=True)

    pocket = models.DecimalField(max_digits=10, decimal_places=2, null=True) 

    endpocketdate=models.DateTimeField(null=True)
    joined_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    status={
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),

    }
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,null=True)
    latitude_of_drop = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude_of_drop = models.DecimalField(max_digits=9, decimal_places=6)
    car_type=models.CharField(max_length=30)
    status=models.CharField(max_length=50,choices=status)
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
        return f'{self.driver.name if self.driver else "No driver"}/{self.customer.name}'
    
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
        
        if self.status == 'B' and self.started_at is None:
            self.started_at = now()

        if self.status == 'F' and self.ended_at is None:
            self.ended_at = now()

        if self.started_at and self.ended_at:
            self.time = (self.ended_at - self.started_at).total_seconds() / 60

        super().save(*args, **kwargs)



class DriversReview(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE,related_name='driver_rating')
    Transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    comment=models.TextField()
    review=models.IntegerField(choices=[(i, i) for i in range(1,6)])
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.driver.name}/{self.customer.name}'

class CutomersReview(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE ,related_name='customer_ratings')
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE)
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    comment=models.TextField()
    review=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.driver.name}/{self.customer.name}'

class Cards(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)    
    center=models.CharField(max_length=20)
    card_id=models.CharField(max_length=25)
    price=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.card_id}/{self.customer.name}'

class Proposal(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    driver=models.ForeignKey(Drivers,on_delete=models.CASCADE)
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    price=models.FloatField()
    comment=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.driver.name}/{self.customer.name}-{self.date}'
    
