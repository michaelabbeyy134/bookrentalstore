from django.shortcuts import render,redirect,get_object_or_404
from bookrentalstore.models import Book,Rental
from bookrentalstore.forms import RentalForm,UserRegistrationForm,UserLoginForm,BookForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now





@login_required(login_url='login')
def available_books(request):
    books = Book.objects.filter(available=True) 
    return render(request, 'bookrentalstore/available_books.html', {'books': books})

@login_required(login_url='login')
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    rented_on = now()
    
    
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.book = book
            rental.user = request.user
            rental.rented_on = rented_on
            rental.save()
            book.available = False  
            book.save()
            return redirect('rental_success',book_id=book.id,rental_id=rental.id)
        
    else:
        form = RentalForm()
    return render(request, 'bookrentalstore/rent_book.html', {'form': form, 'book': book, 'rented_on': rented_on})


# @login_required(login_url='login')
def index(request):
    return render(request,'bookrentalstore/index.html')



def login_view(request):
      
  if request.method == 'POST':
      form = UserLoginForm(request.POST)
      if form.is_valid():      
         username = request.POST['username']
         password = request.POST['password']
         
    #   authentication of user 
         user  = authenticate(username=username,password=password)
         if user:
                login(request,user)
                messages.success(request,f'{user} login succesful')
                return redirect('available_books')
         else:
                messages.error(request, 'Incorrect credentials', extra_tags='danger')
                return redirect('login')
      else:
          for field,errors in form.errors.items():
              for error in errors:
                  messages.error(request, f"{field}:{error}", extra_tags='danger')
  else:
      form = UserLoginForm()      
      
      
      
  return render(request, 'bookrentalstore/login.html')    
      
      



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Registration successful')    
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field}:{error}", extra_tags='danger')

    return render(request,   'bookrentalstore/register.html')


def logout_view(request):
    logout(request)
    return redirect('index')




@login_required(login_url='login')
def rental_success(request, book_id,rental_id):
    book = get_object_or_404(Book, id=book_id)
    rental = get_object_or_404(Rental, id=rental_id) 
    
    context = {
        'book':book,
        'rental':rental
    }
    return render(request, 'bookrentalstore/rental_success.html',context)




def user_rentals(request):
    user_rentals = Rental.objects.filter(user=request.user, returned=False)
    return render(request, 'bookrentalstore/user_rentals.html', {'user_rentals': user_rentals})

def add_books(request):
    return render(request, 'bookrentalstore/add_books.html')


@login_required(login_url='login')
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    if request.method == 'POST':
        rental.returned = True 
        rental.book.available = True 
        rental.book.save() 
        rental.save()  
        messages.success(request, f'You have successfully returned {rental.book.title}')
        return redirect('user_rentals')  
    return render(request, 'bookrentalstore/return_book.html', {'rental': rental})





@login_required(login_url='login')
def manage_books(request):
    books = Book.objects.all()  
    return render(request, 'bookrentalstore/manage_books.html', {'books': books})

@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'bookrentalstore/add_book.html', {'form': form})


@login_required(login_url='login')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookrentalstore/edit_book.html', {'form': form, 'book': book})


@login_required(login_url='login')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('manage_books')
    return render(request, 'bookrentalstore/delete_book.html', {'book': book})
