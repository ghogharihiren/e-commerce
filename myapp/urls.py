from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.edit_profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('change-password/',views.change_password,name='change-password'),
#-----------------------------------------Admin------------------------------------------------    
    path('admin-index/',views.admin_index,name='admin-index'),
    path('seller-list/',views.seller_list,name='seller-list'),
    path('buyer-list/',views.buyer_list,name='buyer-list'),
    path('verification/<int:pk>',views.verification,name='verification'),
#----------------------------------------seller----------------------------------------------------    
   path('seller-index/',views.seller_index,name='seller-index'),
   path('add-product/',views.add_product,name='add-product'),
   path('delete-product/<int:pk>',views.delete_product,name='delete-product'),
   path('edit-product/<int:pk>',views.edit_product,name='edit-product'),
   path('my-product/',views.my_product,name='my-product'),
   path('packing/<int:pk>',views.packing,name='packing'),
   path('ready-to-dispatch/<int:pk>',views.ready_to_dispatch,name='ready-to-dispatch'),
   path('on-the-way/<int:pk>',views.on_the_way,name='on-the-way'),
   path('odered-complate/<int:pk>',views.odered_complate,name='odered-complate'),
#-----------------------------------------------buyer-----------------------------------------------
   
   path('view-product/<int:pk>',views.view_product,name='view-product'),
   path('category-list/<str:id>',views.category_list,name='category-list'),
   path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
   path('my-cart/',views.my_cart,name='my-cart'),
   path('remove-to-cart/<int:pk>',views.remove_to_cart,name='remove-to-cart'),
   path('edit-to-cart/<int:pk>',views.edit_to_cart,name='edit-to-cart'),
   path('checkout/',views.checkout,name='checkout'),
   path('my-buy/',views.my_buy,name='my-buy'),
   path('buy-now/<int:pk>',views.buy_now,name='buy-now'),
   path('view-ordered/<int:pk>',views.view_ordered,name='view-ordered'),
   path('search-product/',views.search_product,name='search-product'),
   path('cancel-ordered/<int:pk>',views.cancel_ordered,name='cancel-ordered'),
   path('edit-ordered/<int:pk>',views.edit_ordered,name='edit-ordered'),
   

   
   
 
]
