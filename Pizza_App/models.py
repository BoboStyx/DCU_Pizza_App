from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

# Create your models here.
class Size(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=50, default="Small")
    price = models.FloatField(default=9.50)

    def __str__(self):
        return self.size

class Crust(models.Model):
    id = models.AutoField(primary_key=True)
    crust = models.CharField(max_length=50, default="Normal")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.crust

class Sauce(models.Model):
    id = models.AutoField(primary_key=True)
    sauce = models.CharField(max_length=50, default="Tomato")
    price = models.FloatField(default=0.50)

    def __str__(self):
        return self.sauce

class Topping(models.Model):
    id = models.AutoField(primary_key=True)
    topping = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.topping

class Cheese(models.Model):
    id = models.AutoField(primary_key=True)
    cheese = models.CharField(max_length=50, default="Mozarella")
    price = models.FloatField(default=0.5)

    def __str__(self):
        return self.cheese

class Pizza(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping, blank=True, default=None)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)

    def Toppings(self):
        return [t.topping for t in self.topping.all()]

    def Total_Price(self):
        toppings = sum(t.price for t in self.topping.all())
        pricing = self.size.price + self.crust.price + self.sauce.price + toppings + self.cheese.price
        return f"{pricing:.2f}"

    def __str__(self):
        toppings = [t.topping for t in self.topping.all()]
        if toppings:
            string_toppings = "Toppings for the Pizza: " + ", ".join(toppings) + "."
        else:
            string_toppings = ""
        return f"A {self.size}-sized Pizza with a {self.crust} Crust and {self.sauce} Sauce. {string_toppings}"

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    first_address = models.CharField(max_length=100)
    second_address = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=50)
    eircode = models.CharField(max_length=8)

    def __str__(self):
        if self.second_address is not None:
            return f"{self.name}, {self.first_address}, {self.second_address},{self.town}, {self.eircode}"
        else:
            return f"{self.name}, {self.first_address}, {self.town}, {self.eircode}"

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, blank=True)

    def total_price(self):
        return f"{sum(float(pizza.Total_Price()) for pizza in self.pizzas.all()): .2f}"

    def __str__(self):
        return f"Cart of {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def total_price(self):
        total = sum(float(p.Total_Price()) for p in self.pizza.all())
        return f"{total:.2f}"

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
      
class Payment_Model(models.Model):
    today = datetime.today()
    id = models.AutoField(primary_key=True)
    name_of_card_owner = models.CharField(max_length=100)
    card_number = models.IntegerField(validators=[MaxValueValidator(9999999999999999)])
    cvv = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(1)])
    expiry_month = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(today.month)])
    expiry_year = models.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(today.year)])
