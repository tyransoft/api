from rest_framework import serializers
from .models import *

class DriversReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriversReview
        fields = '__all__'

class DriversSerializers(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields ='__all__'


class RidesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'




class CustomersReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = CutomersReview
        fields = '__all__'

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields ='__all__'





class ProposalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
