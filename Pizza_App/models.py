from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Size(models.Model):
    size = models.CharField(max_length=50, default="Small")
    price = models.FloatField(default=9.50)

    def __str__(self):
        return self.size

class Crust(models.Model):
    crust = models.CharField(max_length=50, default="Normal")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.crust

class Sauce(models.Model):
    sauce = models.CharField(max_length=50, default="Tomato")
    price = models.FloatField(default=0.50)

    def __str__(self):
        return self.sauce

class Topping(models.Model):
    topping = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.topping

class Cheese(models.Model):
    cheese = models.CharField(max_length=50, default="Mozarella")
    price = models.FloatField(default=0.5)

    def __str__(self):
        return self.cheese

class Pizza(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping, blank=True, default=None)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)

    def allToppings(self):
        return [t.topping for t in self.topping.all()]

    def totalPrice(self):
        toppings = sum(t.price for t in self.topping.all())
        return self.size.price + self.crust.price + self.sauce.price + toppings + self.cheese.price

    def __str__(self):
        toppings = [t.topping for t in self.topping.all()]
        string_toppings = ", ".join(toppings)
        return f"A {self.size} pizza with {self.crust} crust and {self.sauce} sauce. With the following toppings: {string_toppings}."

class Address(models.Model):
    COUNTIES = [
        ('Ant', 'Antrim'), ('Arm', 'Armagh'), ('Car', 'Carlow'), ('Cav', 'Cavan'),
        ('Cla', 'Clare'), ('Cor', 'Cork'), ('Der', 'Derry'), ('Don', 'Donegal'),
        ('Dow', 'Down'), ('Dub', 'Dublin'), ('Fer', 'Fermanagh'), ('Gal', 'Galway'),
        ('Ker', 'Kerry'), ('Kil', 'Kildare'), ('Kil', 'Kilkenny'), ('Lao', 'Laois'),
        ('Lei', 'Leitrim'), ('Lim', 'Limerick'), ('Lon', 'Longford'), ('Lou', 'Louth'),
        ('May', 'Mayo'), ('Mea', 'Meath'), ('Mon', 'Monaghan'), ('Off', 'Offaly'),
        ('Ros', 'Roscommon'), ('Sli', 'Sligo'), ('Tip', 'Tipperary'), ('Tyr', 'Tyrone'),
        ('Wat', 'Waterford'), ('Wes', 'Westmeath'), ('Wex', 'Wexford'), ('Wic', 'Wicklow')
    ]

    name = models.CharField(max_length=100)
    first_address = models.CharField(max_length=100)
    second_address = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=50, choices=COUNTIES)
    town = models.CharField(max_length=50)
    eircode = models.CharField(max_length=8)

    def __str__(self):
        if self.second_address is not None:
            return f"{self.name}, {self.first_address}, {self.second_address},{self.town}, {self.county}, {self.eircode}"
        else:
            return f"{self.name}, {self.first_address}, {self.town}, {self.county}, {self.eircode}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, blank=True)

    def total_price(self):
        return sum(pizza.totalPrice() for pizza in self.pizzas.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def total_price(self):
        return sum(p.totalPrice() for p in self.pizza.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"