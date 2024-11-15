from django.contrib import admin
from django.contrib.auth.models import User
from .models import Name, Categories, AccountPassword

# Register your models here.
admin.site.register(Name)
admin.site.register(Categories)
admin.site.register(AccountPassword)