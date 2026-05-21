from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)  


    def __str__(self):
        return self.title



class Rental(models.Model):
    user_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=14)) 
    rented_on = models.DateTimeField(default=timezone.now) 
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name}  rented {self.book.title}"
    


    