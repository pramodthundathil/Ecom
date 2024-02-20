from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(ProductDetails)
admin.site.register(CartItems)
admin.site.register(CheckoutItems)
admin.site.register(CheckoutAddress)
