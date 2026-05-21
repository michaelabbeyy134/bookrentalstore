from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from bookrentalstore.models import Rental,Book




class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=13)


    class Meta:
        model= User 
        fields= ['first_name','last_name','username','phone_number','password1','password2',]
        
        
        
class UserLoginForm(forms.ModelForm):


    class Meta:
        model = User 
        fields= ['username','password']

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            if not authenticate(username=username,password=password):
                raise forms.ValidationError('Check username or password well')

        
        
        
class RentalForm(forms.ModelForm):
    
    class Meta:
        model = Rental
        fields = ['user_name','phone_number']
        
        
        


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'available','pdf']


        