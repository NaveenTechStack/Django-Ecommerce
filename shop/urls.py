from django.urls import path,include
from django.contrib.auth import views as auth_views
from shop.form import MyPasswordChangeForm, MyPasswordResetForm, MysetPasswordForm

from . import views
urlpatterns = [

    #home
    path('',views.home,name="home"),
   
    #collections  
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionview,name="collections"),
    path('product_details/<str:cname>/<str:pname>',views.product_details,name="product_details"),

    #cart
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('pluscart/',views.plus_cart,name="pluscart"),
    path('minuscart/',views.minus_cart,name="minuscart"),

    #checkout
    path('checkout',views.checkout.as_view(),name="checkout"),
    path('paymentdone',views.paymentdone,name="paymentdone"),

    #orders
    path('orders',views.orders,name="orders"),


    #favourites
    path('fav',views.fav_page,name="fav"),
    path('favourites',views.fav_view_page,name="favourites"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),

    #login
    path('login',views.login_page,name="login_page"),
    path('logout',views.logout_page,name="logout_page"),
    path('register',views.register,name="register"),  

    # profile
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('address',views.address,name="address"),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name="updateAddress"),
    path('passwordchange',
         auth_views.PasswordChangeView.as_view(template_name="shop/profile/changepassword.html",
         form_class=MyPasswordChangeForm,success_url='/login'),name="passwordchange"),

    # forgotPassword
    path('password-reset',
         auth_views.PasswordResetView.as_view(template_name="shop/forgotPassword/password_reset.html",form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name="shop/forgotPassword/password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_confirm.html",form_class=MysetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="shop/forgotPassword/password_reset_complete.html"),name='password_reset_complete')
]
