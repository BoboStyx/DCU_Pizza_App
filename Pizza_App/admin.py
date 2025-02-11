from django.contrib import admin
from .models import Pizza, Size, Sauce, Cheese, Topping, Crust, Order

# Register your models here.
admin.site.register(Size)

admin.site.register(Crust)

admin.site.register(Topping)

admin.site.register(Sauce)

admin.site.register(Cheese)

admin.site.register(Pizza)

class Table_Pizza(admin.TabularInline):
    model = Order.pizza.through 
    extra = 0 

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'address')
    table_pizza = [Table_Pizza]
    exclude = ('pizza',)

admin.site.register(Order, OrdersAdmin)