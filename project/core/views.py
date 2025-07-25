from .serializers  import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal ,InvalidOperation
from django.db.models import Avg,Count
from  django.utils.timezone import now

@api_view(['GET'])
def home(request):
 """it shows home page data"""
 try:
    try:
      if request.user.is_authenticated:
 
        customer = Customers.objects.get(user=request.user)
               
        rides = Transaction.objects.filter(customer=customer,status='A')
        onrode=Transaction.objects.filter(customer=customer,status='B')
        if rides.exists():
            proposals = Proposal.objects.filter(transaction__in=rides)  

            serializer = ProposalSerializers(proposals, many=True)

                
            return Response({
                    'onrode':RidesSerializers(onrode).data if onrode else None,
                    'proposals': serializer.data if proposals else None,
                })
      else:
        customer = None
           
    except Customers.DoesNotExist:
        customer = None

    try:
      if request.user.is_authenticated:

        driver = Drivers.objects.get(user=request.user)
            
        open_rides = Transaction.objects.filter(car_type=driver.car_type, status='A')
        onrode = Transaction.objects.filter(driver=driver, status='B')
        sub=Subscription.objects.get(driver=driver)
        plans=Plan.objects.all()
        return Response({
                    'openrides':RidesSerializers(open_rides, many=True).data if open_rides else None,
                    'onrode': RidesSerializers(onrode).data if onrode else None,
                    'plans':  PlansSerializers(plans,many=True).data if not sub else None,
                    'renew':'عليك تجديد الاشتراك الخاص بك' if sub.is_active == False else None,
        })
      else:
        driver = None
   
    except Drivers.DoesNotExist:
                driver = None

    if  customer==None and  driver ==None:
        plans=Plan.objects.all()

        return Response({'plans':  PlansSerializers(plans,many=True).data })


 except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)


@api_view(['POST'])
def generate_cards(request):
   """allows admin to generate payment cards"""
   try:
      if request.user.is_authenticated:
         data=request.data
         value=data.get('value')
         number_of_cards=data.get('number_of_cards')
         if not number_of_cards or not value:
           return Response({'error':'عدد الكروت والقيمة بيانات مطلوبة'},status=400)
         cards=Cards.generate_cards(number_of_cards,value)
         
         return Response({'message':'تم انشاء الكروت بنجاح'},status=200)

   except Exception as a:
      return Response({'error':str(a)})
  
@api_view(['POST','GET'])
def card_list_view(request):
    value_filter = None
    is_used_filter = None

    if request.method == "GET":
        value_filter = request.query_params.get('value')
        is_used_filter = request.query_params.get('is_used')
    elif request.method == "POST":
        value_filter = request.data.get('value')
        is_used_filter = request.data.get('is_used')

    if value_filter and not is_used_filter:
        cards = Cards.objects.filter(value=value_filter)  
        shows=CardsSerializers(cards,many=True)       
    
    elif is_used_filter and not value_filter:
        is_used_filter = is_used_filter.lower() == 'true'  
        cards = Cards.objects.filter(is_used=is_used_filter)  
        shows=CardsSerializers(cards,many=True)       

    elif value_filter and is_used_filter:
        is_used_filter = is_used_filter.lower() == 'true'  
        cards = Cards.objects.filter(is_used=is_used_filter,value=value_filter) 
        shows=CardsSerializers(cards,many=True)       

    else:
        cards=Cards.objects.all()
        shows=CardsSerializers(cards,many=True)       
    return Response(shows.data)

@api_view(['POST'])
def add_plan(request):
     try:
        name=request.data.get('name')
        duration=request.data.get('duration')
        price=request.data.get('price')
        description=request.data.get('description')
        if name and duration and description and price:
           plan=Plan.objects.create(
              name=name,
              price=price,
              description=description,
              duration=duration,

           )
           plan.save()
           return Response({'message':'تمت اضافة الباقة بنجاح !'})
        else:
           return Response({'error':'جميع البيانات مطلوبة !'})
           
     except Exception as e:
        return Response({'error':str(e)})  
@api_view(['GET','POST'])     
def update_plan(request, plan_id):
    try:
      plan=Plan.objects.get(id=plan_id)
      if plan:
            old_plan_data = PlansSerializers(plan).data
                
            plan.name = request.data.get('name', plan.name)
            plan.price = request.data.get('price', plan.price)
            plan.duration = request.data.get('duration', plan.duration)
            plan.description = request.data.get('description', plan.description)
 
            plan.save()

            updated_plan_data =  PlansSerializers(plan).data
            return Response({
                'old_data': old_plan_data,
                'updated_data': updated_plan_data,
                })
    except Exception as e:
        return Response({'error':str(e)})  
@api_view(['GET'])    
def plans(request):
   plans=Plan.objects.all()
   plan_list=PlansSerializers(plans,many=True)
   return Response(plan_list.data)




@api_view(['POST'])
def update_user_location(request):
   """update users locations constantly"""
   try:
    if  request.user.is_authenticated:

      data=request.data
      latitude=data.get('latitude')
      longitude=data.get('longitude')
      if not latitude or not longitude:
         return Response({'error':'احداثيات خطوط الطول والعرض مطلوبة'},status=400)
      
      try:
         latitude = Decimal(latitude)  
         longitude = Decimal(longitude)
      except ValueError:
            return Response({'error': 'الإحداثيات غير صحيحة'},status=400)
      try:
         driver=Drivers.objects.get(user=request.user) 

         driver.latitude=latitude
         driver.longitude=longitude
         driver.save()
      
      except Drivers.DoesNotExist:
         driver = None
      try:
         customer=Customers.objects.get(user=request.user) 

         customer.latitude=latitude
         customer.longitude=longitude
         customer.save()
      
      except Customers.DoesNotExist:
         customer = None
      if customer == None and driver ==None:
      
       return Response({'error':'لم يتم التعرف عليك  حاول تسجيل الدخول'}, status=400)
           
      
      
      return Response({'message':'تم تحديت موقعك بنجاح',})
    else:
      return Response({'error':'لم يتم التعرف عليك  حاول تسجيل الدخول'}, status=400)
  
   except Exception as a:
      return Response({'error':str(a)})



@api_view(['POST'])
def request_ride(request):
   """allow customer to post a ride request"""
   try:
    if request.user.is_authenticated:
      data = request.data
      customer_id = data.get('customer')
      
      latitude_str = data.get('latitude_of_drop', '0')  
      longitude_str = data.get('longitude_of_drop', '0')
            
      try:
         latitude = Decimal(latitude_str)  
         longitude = Decimal(longitude_str)
      except ValueError:
            return Response({'error': 'الإحداثيات غير صحيحة'},status=400)
      
      report = data.get('description')
      weight = data.get('weight')
      car_type = data.get('car_type')

      try:
         customer = Customers.objects.get(id=customer_id)
      except Customers.DoesNotExist:
            return Response({'error': 'العميل غير موجود في قاعدة البيانات.'}, status=404)

      if customer.status == 'available':
         ride = Transaction.objects.create(
             customer=customer,
             status='A',
             longitude_of_drop=longitude,
             latitude_of_drop=latitude,
             car_type=car_type,
             description=report,
             weight=weight,
         )
         ride.save() 
         customer.status = 'onride'
         customer.save()
         return Response({'message': 'تم انشاء رحلة بنجاح'}, status=200)
      else:
         return Response({'error': 'انت في رحلة مسبقا عليك انهائها اولا للتمكن من طلب رحلة جديدة'}, status=400)
    
    else:
         return Response({'error': 'لم يتم التعرف عليك  حاول تسجيل الدخول'}, status=400)

   except Exception as a:
      return Response({'error': str(a)})

@api_view(['GET'])
def show_rides(request):
   """show rides that suitable for the driver"""
   try:
     if  request.user.is_authenticated:

      
      driver=Drivers.objects.get(user=request.user)
      if driver:
         if driver.status == 'available':
           rides=Transaction.objects.filter(car_type=driver.car_type,status='A')        
           shows=RidesSerializers(rides,many=True)       
           return Response(shows.data)
         
         else:
          return Response({'message': 'انت في رحلة الان يجب عليك انهائها للحصول على رحلات جديدة'}, status=400)

      else:
         return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
     else:
       return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
 
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)



@api_view(['POST'])
def make_proposal(request):
  """allow drivers to send proposals to customers who want a ride"""
  try:
   if  request.user.is_authenticated:

     data=request.data
     id=data.get('ride_id')
     comment=data.get('comment')
     price=data.get('price')
     driver = Drivers.objects.get(user=request.user)
     sub=Subscription.objects.get(deriver=driver)
     if driver:
      if sub.end_date <= timezone.now().date():
        sub.is_active = False
        sub.save()
        sub.driver.status = "available"
        sub.driver.save()
        if sub.is_active:
        
         ride=Transaction.objects.get(id=id)
         proposal=Proposal.objects.create(
           driver=driver,
           transaction=ride,
           price=price,
           comment=comment,
           customer=ride.customer,
         ) 
         proposal.save()
         return Response({'message':'تم ارسال الطلب بنجاح'}, status=200)
      return Response({'error':'ليس لديك اشتراك فعال !!! '}, status=400)

     return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


   else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
  except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)



@api_view(['GET'])
def show_proposal(request):
   """show proposals to customer """
   try:
      if request.user.is_authenticated:
            customer = Customers.objects.get(user=request.user)  

            rides = Transaction.objects.filter(customer=customer, status='A')

            if rides.exists():
                proposals = Proposal.objects.filter(transaction__in=rides)  

                serializer = ProposalSerializers(proposals, many=True)

                
                return Response(serializer.data, status=200)
               
            else:
                return Response({'error': 'لا توجد رحلات متاحة حالياً لهذا العميل.'}, status=400)

      else:
            return Response({'error': 'لم يتم التعرف عليك كعميل، حاول تسجيل الدخول أولاً'}, status=400)

   except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ البيانات: {str(e)}'}, status=500)



@api_view(['POST'])
def confirm_ride(request):
    try:
        if request.user.is_authenticated:
            customer = Customers.objects.get(user=request.user)
            proposal_id = request.data.get('proposal_id')

            if not proposal_id:
                return Response({'error': 'مفقود معرّف الاقتراح'}, status=400)

            try:
                proposal = Proposal.objects.get(id=proposal_id)
            except Proposal.DoesNotExist:
                return Response({'error': 'الاقتراح غير موجود'}, status=404)

            try:
                ride = Transaction.objects.get(customer=customer, status='A')
            except Transaction.DoesNotExist:
                return Response({'error': 'لا يوجد معاملة نشطة لتأكيد الرحلة'}, status=404)

            try:
                driver = Drivers.objects.get(id=proposal.driver.id)
            except Drivers.DoesNotExist:
                return Response({'error': 'السائق غير متاح'}, status=400)

            if proposal.price is None:
                return Response({'error': 'السعر غير موجود'}, status=400)

            try:
                proposal_price = Decimal(str(proposal.price))  
            except InvalidOperation:
                return Response({'error': 'قيمة السعر غير صالحة، تم استخدام قيمة  0'}, status=400)

            if driver.status == 'available':
                Transaction.objects.filter(id=ride.id).update(
                    driver=driver,
                    price=proposal_price,
                    status='B',
                    started_at=now(),
                )

                Drivers.objects.filter(id=driver.id).update(
                    status='driving'
                )

                return Response({'message': 'تم تأكيد الرحلة بنجاح، سيتواصل معك السائق قريبًا.'})
            else:
                return Response({'error': 'السائق غير متاح حاليا.'}, status=400)

        return Response({'error': 'لم يتم التعرف عليك. حاول تسجيل الدخول أولاً.'}, status=400)

    except Exception as e:
        return Response({'error': f'حدث خطأ أثناء معالجة الطلب: {str(e)}'}, status=500)

@api_view(['POST'])
def customer_review(request):
   """it allows customer to make reviews about drivers"""
   try:
    if  request.user.is_authenticated:
      
      comment=request.data.get('comment')
      ride_id=request.data.get('ride_id')
      review=request.data.get('review')
      customer=Customers.objects.get(user=request.user)
      if customer:
        ride=Transaction.objects.get(id=ride_id)
        createreview=DriversReview.objects.create(
           customer=customer,
           driver=ride.driver,
           Transaction=ride,
           comment=comment,
           review=review,
           )
        createreview.save()


        return Response({'message':'قيََمت السائق بنجاح نشكرك على ذلك'})
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


    else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)

@api_view(['POST'])
def driver_review(request):
   """it allows driver to make reviews about customers"""
   try:
    if  request.user.is_authenticated:
      
      comment=request.data.get('comment')
      ride_id=request.data.get('ride_id')
      review=request.data.get('review')
      driver=Drivers.objects.get(user=request.user)
      if driver:
        ride=Transaction.objects.get(id=ride_id)
        createreview=CutomersReview.objects.create(
           customer=ride.customer,
           driver=driver,
           transaction=ride,
           comment=comment,
           review=review,
           )
        createreview.save()


        return Response({'message':'قيََمت العميل بنجاح نشكرك على ذلك'})
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


    else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)

@api_view(['POST'])
def drivers_canceling(request):
   """it allows driver to cancele rides"""
   try:
    if  request.user.is_authenticated:
      ride_id=request.data.get('ride_id')
      driver=Drivers.objects.get(user=request.user)
      if driver:
        ride=Transaction.objects.get(id=ride_id)
        Transaction.objects.filter(id=ride_id).update(status='D',ended_at=now(),time = ( now() - ride.started_at).total_seconds() / 60)
        Drivers.objects.filter(id=ride.driver.id).update(status='available')
        Customers.objects.filter(id=ride.customer.id).update(status='available')
  

        return Response({'message':'الغيت الرحلة بنجاح'})
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


    else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)
@api_view(['POST'])
def customers_canceling(request):
    """it allows customers to cancel rides"""
    try:
        if request.user.is_authenticated:
            ride_id = request.data.get('ride_id')
            customer = Customers.objects.get(user=request.user)
            ride = Transaction.objects.get(id=ride_id)

            if customer:
                Transaction.objects.filter(id=ride_id).update(status='C',ended_at=now(),time = ( now() - ride.started_at).total_seconds() / 60)
                
                Drivers.objects.filter(id=ride.driver.id).update(status='available')
                
                Customers.objects.filter(id=ride.customer.id).update(status='available')

                return Response({'message': 'تم إلغاء الرحلة بنجاح'})
            else:
                return Response({'error': 'العميل غير موجود أو غير صالح'}, status=404)
        
        else:
            return Response({'error': 'لم يتم التعرف عليك، حاول تسجيل الدخول أولاً'}, status=400)

    except Customers.DoesNotExist:
        return Response({'error': 'العميل غير موجود في قاعدة البيانات'}, status=404)
    except Transaction.DoesNotExist:
        return Response({'error': 'الرحلة غير موجودة'}, status=404)
    except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ البيانات: {str(e)}'}, status=500)

@api_view(['GET'])
def driver_data(request,driver_id):
   """it gives driver's info to customer """
   try:
    driver=Drivers.objects.get(id=driver_id)

    driverdata=DriversSerializers(driver,many=False)
    return Response(driverdata.data)
   except Exception as e:
    return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)
   

@api_view(['POST'])
def driver_deliver(request):
   """it allows driver to deliver rides"""
   try:
    if  request.user.is_authenticated:
      ride_id=request.data.get('ride_id')
      driver=Drivers.objects.get(user=request.user)
      if driver:
         Transaction.objects.filter(id=ride_id).update(status='E')
         return Response({'message':'تم تسليم الرحلة في انتظار تاكيد العميل'})
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


    else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)

@api_view(['POST'])
def deliver_confirmation(request):
   """it allows customers to end rides"""
   try:
    if  request.user.is_authenticated:
      user=request.user
      ride_id=request.data.get('ride_id')
      customer=Customers.objects.get(user=user)
      if customer:
        ride=Transaction.objects.get(id=ride_id)
        if ride.status =='E':

         Transaction.objects.filter(id=ride_id).update(status='E',ended_at=now(),time = ( now() - ride.started_at).total_seconds() / 60)
         Drivers.objects.filter(id=ride.driver.id).update(status='available')
         Customers.objects.filter(id=ride.customer.id).update(status='available')
  
        return Response({'message':'تم انهاء الرحلة بنجاح '})
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)


    else:
      return Response({'error':'لم يتم التعرف عليك كسائق حاول تسجيل الدخول'}, status=400)
              
   except Exception as e:
      return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)

@api_view(['GET'])
def profile(request):
   """it shows the profile of the user"""
   try:
        if request.user.is_authenticated:
            try:
                customer = Customers.objects.get(user=request.user)
                ratings = CutomersReview.objects.filter(customer=customer)
                customer = Customers.objects.annotate(
                    ratings_count=Count('customer_ratings'),
                    ratings_average=Avg('customer_ratings__review')
                ).get(user=request.user)
                rides = Transaction.objects.filter(customer=customer).count()
                return Response({
                    'user': CustomerSerializers(customer).data,
                    'ratings': CustomersReviewSerializers(ratings, many=True).data,
                    'ratings_count': customer.ratings_count,
                    'ratings_average': round(customer.ratings_average, 2) if customer.ratings_average else 0,
                    'transaction_count': rides,
                })
            except Customers.DoesNotExist:
                customer = None

            try:
                driver = Drivers.objects.get(user=request.user)
                ratings = DriversReview.objects.filter(driver=driver)
                driver = Drivers.objects.annotate(
                    ratings_count=Count('driver_rating'),
                    ratings_average=Avg('driver_rating__review')
                ).get(user=request.user)
                rides = Transaction.objects.filter(driver=driver).count()
                sub_info=Subscription.objects.get(driver=driver)
                return Response({
                    'user': DriversSerializers(driver).data,
                    'ratings': DriversReviewSerializers(ratings, many=True).data,
                    'ratings_count': driver.ratings_count,
                    'ratings_average': round(driver.ratings_average, 2) if driver.ratings_average else 0,
                    'transaction_count': rides,
                    'sub_info':SubSerializers(sub_info).data if sub_info else None,
                    'remaining_days':sub_info.remaining_days() if sub_info else None,
                })
            except Drivers.DoesNotExist:
                driver = None

            if not customer and not driver:
                return Response({'error': 'لم يتم التعرف عليك كسائق أو عميل. حاول تسجيل الدخول'}, status=400)

        else:
            return Response({'error': 'لم يتم التعرف عليك. حاول تسجيل الدخول'}, status=400)

   except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=500)



@api_view(['PUT'])
def update_profile(request):
    """ update user profile and show old data before the update"""
    try:
        if request.user.is_authenticated:
            customer = None
            driver = None
            
            try:
                customer = Customers.objects.get(user=request.user)
            except Customers.DoesNotExist:
                customer = None

            try:
                driver = Drivers.objects.get(user=request.user)
            except Drivers.DoesNotExist:
                driver = None

            if customer:
                old_customer_data = CustomerSerializers(customer).data
                
                customer.gender = request.data.get('gender', customer.gender)
                customer.phone = request.data.get('phone', customer.phone)
                customer.image = request.data.get('image', customer.image)
                customer.born_date = request.data.get('born_date', customer.born_date)
 
                customer.save()

                updated_customer_data = CustomerSerializers(customer).data
                return Response({
                    'old_data': old_customer_data,
                    'updated_data': updated_customer_data,
                })

            elif driver:
                old_driver_data = DriversSerializers(driver).data
                
                driver.phone = request.data.get('phone', driver.phone)
                driver.car_image = request.data.get('car_image', driver.car_image)
                driver.profile_image = request.data.get('profile_image', driver.profile_image)
                driver.profile_image = request.data.get('proof_image', driver.profile_image)


                driver.license_image = request.data.get('license_image', driver.license_image)
                driver.car_type = request.data.get('car_type', driver.car_type)
                driver.car_id = request.data.get('car_id', driver.car_id)
                driver.national_number=request.data.get('national_number', driver.national_number)
                driver.license_id=request.data.get('license_id', driver.license_id)
                driver.born_date=request.data.get('born_date', driver.born_date)
                driver.national_number=request.data.get('national_number', driver.national_number)



                driver.save()

                updated_driver_data = DriversSerializers(driver).data
                return Response({
                    'old_data': old_driver_data,
                    'updated_data': updated_driver_data,
                })

            else:
                return Response({'error': 'لم يتم التعرف عليك كسائق أو عميل. حاول تسجيل الدخول'}, status=400)

        else:
            return Response({'error': 'لم يتم التعرف عليك. حاول تسجيل الدخول'}, status=400)

    except Exception as e:
        return Response({'error': f'حدث خطأ أثناء حفظ البيانات : {str(e)}'}, status=400)




@api_view(['POST'])
def wallet_charging(request):
    """it allows drivers to charg their wallets"""
    if request.user.is_authenticated:
 
      driver=Drivers.objects.get(user=request.user)
      if driver:
        card_code = request.data.get('code')
        card=Cards.objects.get(code=card_code)
        if card:
            if card.is_used == False:
                driver.pocket= driver.pocket + card.value
                driver.save()
                card.is_used=True
                card.save()
                return Response(f'تم  شحن محفظتك بقيمة {card.value}',status=200)
            
            return Response({'error':'رقم بطاقة التعبئة هذه مستعمل مسبقا  يرجى التاكد من صحته والمحاولة مجددا'},status=400)
        return Response({'error':'الرقم السري غير صحيح'},status=400)
      return Response({'error':'لم نتعرف عليك كسائق حاول مجددا'},status=400)

    return Response({'error':'لم نتعرف عليك كسائق حاول مجددا'},status=400)







@api_view(['POST'])
def buy_plan(request, plan_id):
        """it allows drivers to buy a plan"""
        if request.user.is_authenticated:
            driver = Drivers.objects.get(user=request.user)
            plan = Plan.objects.get(id=plan_id)

            if Subscription.objects.filter(driver=driver).exists():
                return Response({'error':'لديك اشتراك فعال بالفعل'},status=400)
                

         

            if driver.pocket >= plan.price:
                subscription = Subscription.objects.create(
                    driver=driver,
                    plan=plan,
                    final_price=plan.price
                )
                
               
                subscription.save()
                driver.pocket -= plan.price
                driver.status = 'available'
                driver.save()

                return Response({'message':'تم شراء الاشتراك بنجاح!'},status=200)
            else:
                return Response({'error':'رصيدك غير كافٍ لإتمام عملية الشراء'},status=400)
        else:
            return Response({'error':'عليك تسجيل الدخول او انشاء حساب لاتمام هذه العملية'})

   
@api_view(['POST'])    
def renew_subscription(request, subscription_id):
  """it allows drivers to renew their subscriptions"""
  if request.user.is_authenticated:
 
    subscription = Subscription.objects.get(id=subscription_id)
    driver =subscription.driver

    if subscription.is_active == False:
        if driver.pocket >= subscription.final_price:

    

          start = timezone.now().date()

          subscription.start_date=start
          subscription.is_active=True
          subscription.save()

          driver.status = 'available'
          driver.pocket -=  subscription.final_price
          
          driver.save()

          return Response( {'message':'تم تجديد اشتراكك بنجاح  !'},status=200)

        
        return Response({'error':' القيمة التي في محفظتك غير كافية لتجديد الاشتراك , يرجى شحن المحفظة بالقيمة المناسبة'},status=400)
    else:
     return Response({'error':'الاشتراك الخاص بك لايزال فعالا'},status=400)
  else:
            return Response({'error':'عليك تسجيل الدخول او انشاء حساب لاتمام هذه العملية'},status=400)
