from core.serializers import *
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from decimal import Decimal
from django.middleware.csrf import get_token




@api_view(['POST'])
def register_driver(request):
  if request.user.is_authenticated:
      return Response({'error': 'انت مسجل بالفعل'}, status=500) 

  else:
   name=request.data.get('name')
   email=request.data.get('email')
   password=request.data.get('password')    
   driver_data=request.data.get('driver')

   if not name  or not password or not email or not driver_data:
      return Response({'error': 'جميع الحقول مطلوبة:  عنوان البريد الالكتروني، الاسم، كلمة المرور، وباقي البيانات مطلوبة .'}, status=400)
   if User.objects.filter(username=email).exists():
      return Response({'error': 'البريد الالكتروني هذا موجود بالفعل! حاول تسجيل الدخول'},status=400)

   try:
      user = User.objects.create_user(username=email,first_name=name ,password=password, email=email)
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء إنشاء الحساب: {str(e)}'}, status=500)
   latitude=driver_data.get('latitude')
   longitude=driver_data.get('longitude')
   lat=Decimal(latitude)
   long=Decimal(longitude)    
       
   driver = Drivers(
        user=user,
        phone=driver_data.get('phone'),
        profile_image=driver_data.get('profile_image'),
        car_image=driver_data.get('car_image'),
        proof_image=driver_data.get('proof_image'),
        gender=driver_data.get('gender'),
        license_id=driver_data.get('license_id'),
        national_number=driver_data.get('national_number'),
        license_image=driver_data.get('license_image'),
        car_type=driver_data.get('car_type'),
        car_id=driver_data.get('car_id'),
        born_date=driver_data.get('born_date'),
        status='available',
        latitude=lat,
        longitude=long,
     
    )
   try:
        driver.save()
   except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ بيانات السائق: {str(e)}'}, status=500)
    
   user = authenticate(username=email, password=password)

   if user is not None:
         login(request, user)
         return Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
         

   else:
         return Response({'error': 'فشلت عملية التسجيل، حاول مرة أخرى.'}, status=500)

   
@api_view(['POST'])
def register_customer(request):
  if request.user.is_authenticated:
      return Response({'error': 'انت مسجل بالفعل'}, status=500) 

  else:
   name=request.data.get('name')
   email=request.data.get('email')
   password=request.data.get('password')    
   customer_data=request.data.get('customer')

   if not name or not email or not password or not customer_data:
      return Response({'error': 'جميع الحقول مطلوبة:  البريد الالكتروني، الاسم , كلمة المرور، وباقي البيانات مطلوبة .'}, status=400)
   if User.objects.filter(username=email).exists():
      return Response({'error': 'البريد الالكتروني هذا موجود بالفعل! حاول تسجيل الدخول'},status=400)

   try:
      user = User.objects.create_user(username=email,first_name=name ,password=password, email=email)
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء إنشاء الحساب: {str(e)}'}, status=500)
       
   latitude=customer_data.get('latitude')
   longitude=customer_data.get('longitude')
   lat=Decimal(latitude)
   long=Decimal(longitude)
   customer = Customers(
        user=user,
        gender=customer_data.get('gender'),
        phone=customer_data.get('phone'),
        image=customer_data.get('image'),
        born_date=customer_data.get('born_date'),
        status='available',
        latitude=lat,
        longitude=long,
            )

   try:
      customer.save()
   except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ بيانات العميل: {str(e)}'}, status=500)

   user = authenticate(username=email, password=password)
  
  
   if user is not None:
         login(request, user)
         return Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
 
          
   else:
         return Response({'error': 'فشلت عملية التسجيل، حاول مرة أخرى.'}, status=500)
 
@api_view(['POST'])
def login_user(request):
  if request.user.is_authenticated:
      return Response({'error': 'انت مسجل بالفعل'}, status=500) 

  else:
   email = request.data.get('email')
   password = request.data.get('password')

   if not email or not password:
      return Response({'error': 'اسم المستخدم وكلمة المرور مطلوبين.'}, status=400)

   user = authenticate(username=email,email=email, password=password)

   if user is not None:
      login(request, user)
      return Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
         
 
   return Response({'error': 'اسم المستخدم وكلمة المرور غير صحيحين. حاول مرة أخرى أو يمكنك إنشاء حساب جديد.'}, status=401)

@api_view(['POST'])
def logout_user(request):
   if not request.user.is_authenticated:
      return Response({'error': 'لم تقم بتسجيل الدخول بعد.'}, status=400)

   logout(request)
   return Response({'message': 'تم تسجيل الخروج بنجاح'}, status=200)




@api_view(['POST'])
def change_password(request):    
   email = request.data.get('email')
   old_password = request.data.get('old_password')
   new_password = request.data.get('new_password')

   if not email or not old_password or not new_password:
      return Response({'error': 'جميع الحقول مطلوبة: عنوان البريد الالكتروني ، كلمة المرور القديمة، وكلمة المرور الجديدة.'}, status=400)

   try:
      user = get_user_model().objects.get(username=email)
   except get_user_model().DoesNotExist:
      return Response({'error': 'لم يتم العثور على عنوان البريد الالكتروني. حاول مرة أخرى.'}, status=404)

   if not check_password(old_password, user.password):
      return Response({'error': 'كلمة المرور القديمة خاطئة.'}, status=400)
   
   user.set_password(new_password)
   user.save()
   return Response({'message': 'لقد تم تغيير كلمة المرور بنجاح.'}, status=200)