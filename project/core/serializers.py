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

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['email','first_name']

class CustomerSerializers(serializers.ModelSerializer):
    user=UserSerializers()
    class Meta:
        model = Customers
        fields ='__all__'
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




class ProposalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'


class PlansSerializers(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class CardsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class SubSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
