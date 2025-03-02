from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Works, Category, Vehicles, User, RentTransaction, Review])
