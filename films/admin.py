from django.contrib import admin

# Register your models here.
from .models import Actor,Movie,Comment

admin.site.register([Actor,Movie,Comment])
 
 