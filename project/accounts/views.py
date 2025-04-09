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
   username=request.data.get('username')
   email=request.data.get('email')
   password=request.data.get('password')    
   driver_data=request.data.get('driver')

   if not username  or not password or not driver_data:
      return Response({'error': 'جميع الحقول مطلوبة: اسم المستخدم، الاسم , كلمة المرور، وباقي البيانات مطلوبة .'}, status=400)
   if User.objects.filter(username=username).exists():
      return Response({'error': 'اسم المستخدم هذا مستعمل مسبقا.استعمل اسم مستخدم اخر او يمكنك تسجيل الدخول.'},status=400)
   if User.objects.filter(email=email).exists():
      return Response({'error': 'البريد الالكتروني هذا موجود بالفعل! حاول تسجيل الدخول'},status=400)

   try:
      user = User.objects.create_user(username=username, password=password, email=email)
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء إنشاء الحساب: {str(e)}'}, status=500)
   latitude=driver_data.get('latitude')
   longitude=driver_data.get('longitude')
   lat=Decimal(latitude)
   long=Decimal(longitude)    
       
   driver = Drivers(
        user=user,
        name=driver_data.get('name'),
        phone=driver_data.get('phone'),
        image=driver_data.get('image'),
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
    
   user = authenticate(username=username, password=password)

   if user is not None:
         login(request, user)
         response= Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
         
         response.set_cookie(
             'csrftoken',
             get_token(request),
             httponly=True,
             samesite='lax',
         )
         return response
   else:
         return Response({'error': 'فشلت عملية التسجيل، حاول مرة أخرى.'}, status=500)

@api_view(['POST'])
def register_customer(request):
  if request.user.is_authenticated:
      return Response({'error': 'انت مسجل بالفعل'}, status=500) 

  else:
   username=request.data.get('username')
   email=request.data.get('email')
   password=request.data.get('password')    
   customer_data=request.data.get('customer')

   if not username  or not password or not customer_data:
      return Response({'error': 'جميع الحقول مطلوبة: اسم المستخدم، الاسم , كلمة المرور، وباقي البيانات مطلوبة .'}, status=400)
   if User.objects.filter(username=username).exists():
      return Response({'error': 'اسم المستخدم هذا مستعمل مسبقا.استعمل اسم مستخدم اخر او يمكنك تسجيل الدخول.'},status=400)
   if User.objects.filter(email=email).exists():
      return Response({'error': 'البريد الالكتروني هذا موجود بالفعل! حاول تسجيل الدخول'},status=400)

   try:
      user = User.objects.create_user(username=username, password=password, email=email)
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء إنشاء الحساب: {str(e)}'}, status=500)
       
   latitude=customer_data.get('latitude')
   longitude=customer_data.get('longitude')
   lat=Decimal(latitude)
   long=Decimal(longitude)
   customer = Customers(
        user=user,
        name=customer_data.get('name'),
        phone=customer_data.get('phone'),
        image=customer_data.get('image'),
        status='available',
        latitude=lat,
        longitude=long,
            )

   try:
      customer.save()
   except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ بيانات العميل: {str(e)}'}, status=500)

   user = authenticate(username=username, password=password)
  
  
   if user is not None:
         login(request, user)
         response= Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
         
         response.set_cookie(
             'csrftoken',
             get_token(request),
             httponly=True,
             samesite='lax',
         )
         return response
   else:
         return Response({'error': 'فشلت عملية التسجيل، حاول مرة أخرى.'}, status=500)


@api_view(['POST'])
def login_user(request):
  if request.user.is_authenticated:
      return Response({'error': 'انت مسجل بالفعل'}, status=500) 

  else:
   username = request.data.get('username')
   password = request.data.get('password')

   if not username or not password:
      return Response({'error': 'اسم المستخدم وكلمة المرور مطلوبين.'}, status=400)

   user = authenticate(username=username, password=password)

   if user is not None:
      login(request, user)
      response= Response({
               'message': 'مرحبا بك. تم تسجيلك بنجاح',
               'csrftoken':get_token(request),
              
            },status=200)
         
      response.set_cookie(
             'csrftoken',
             get_token(request),
             httponly=True,
             samesite='lax',
         )
      return response
   return Response({'error': 'اسم المستخدم وكلمة المرور غير صحيحين. حاول مرة أخرى أو يمكنك إنشاء حساب جديد.'}, status=401)



@api_view(['POST'])
def logout_user(request):
   if not request.user.is_authenticated:
      return Response({'error': 'لم تقم بتسجيل الدخول بعد.'}, status=400)

   logout(request)
   return Response({'message': 'تم تسجيل الخروج بنجاح'}, status=200)




@api_view(['POST'])
def change_password(request):    
   username = request.data.get('username')
   old_password = request.data.get('old_password')
   new_password = request.data.get('new_password')

   if not username or not old_password or not new_password:
      return Response({'error': 'جميع الحقول مطلوبة: اسم المستخدم، كلمة المرور القديمة، وكلمة المرور الجديدة.'}, status=400)

   try:
      user = get_user_model().objects.get(username=username)
   except get_user_model().DoesNotExist:
      return Response({'error': 'لم يتم العثور على اسم المستخدم. حاول مرة أخرى.'}, status=404)

   if not check_password(old_password, user.password):
      return Response({'error': 'كلمة المرور القديمة خاطئة.'}, status=400)
   
   user.set_password(new_password)
   user.save()
   return Response({'message': 'لقد تم تغيير كلمة المرور بنجاح.'}, status=200)