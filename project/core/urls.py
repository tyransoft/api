from django.urls import path
from .views import *



urlpatterns = [
    path('',home,name='home'),
    path('generate-cards/',generate_cards,name='generate_cards'),
    path('cards/',card_list_view,name='card_list'),
    path('add-plan/',add_plan,name='add_plan'),
    path('update-plan/<int:plan_id>',update_plan,name='update_plan'),
    path('plans/',plans,name='plan_list'),
    path('renew-subscription/<int:subscription_id>/',renew_subscription,name='renew_subscription'),
    path('buy-plan/<int:plan_id>',buy_plan,name='buy_plan'),
    path('charg-wallet/',wallet_charging,name='charg_wallet'),


    path('request-transaction/',request_ride,name='request_ride'),
    path('available-transactions/',show_rides,name='available_ride'),
    path('update-location/',update_user_location,name='update_location'),
    path('apply-for-transaction/',make_proposal,name='apply'),
    path('show-proposals/',show_proposal,name='show_proposals'),
    path('approve-a-transaction/',confirm_ride,name='confirm_ride'),
    path('add-customer-review/',customer_review,name='customer_review'),
    path('add-driver-review/',driver_review,name='driver_review'),
    path('driver-cancels-transaction/',drivers_canceling,name='drivers_canceling'),
    path('customer-cancels-transaction/',customers_canceling,name='customers_canceling'),
    path('driver-info/<int:driver_id>/',driver_data,name='driver_data'),
    path('profile/',profile,name='profile'),
    path('driver-finishing-ride/',driver_deliver,name='driver_deliver'),
    path('customer-confirm-deliver/',deliver_confirmation,name='customer_deliver'),
    path('update-profile/',update_profile,name='update_profile'),
    

    

]   
