from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ONE TO ONE RELATIONSHIP WITH BUILT-IN USER MODEL ---> IMPLEMENTS NAME FOR THE USER
class Name(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# CATEGORIES TABLE
class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

# PASSWORD TABLE FOR THE DIFFERENT PASSWORDS SAVED BY USER
class AccountPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField(null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return "Password Object"