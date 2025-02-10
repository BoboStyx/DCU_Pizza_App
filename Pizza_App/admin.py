from django.contrib import admin
from .models import Pizza, Size, Sauce, Cheese, Topping, Crust, Orders

# Register your models here.
admin.register(Size)

admin.register(Crust)

admin.register(Topping)

admin.register(Sauce)

admin.register(Cheese)

class Table_Pizza(admin.TabularInline):
    model = Orders.pizza.through 
    extra = 0 

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'address')
    table_pizza = [Table_Pizza]
    exclude = ('pizza',)

admin.site.register(Orders, OrdersAdmin)