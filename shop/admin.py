from django.contrib import admin
from .models import Cart, Category, Customer, OrderPlaced, Payment,Products

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','image','description')
admin.site.register(Category,CategoryAdmin)

admin.site.register(Products)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','product_qty','created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']