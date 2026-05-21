from django.urls import path
from bookrentalstore.views import index,logout_view,login_view,register,available_books,rent_book,rental_success,user_rentals,return_book,manage_books,delete_book,edit_book,add_book
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
     path('index/',index,name= 'index'),
     path('login/',login_view,name='login'),
     path('logout/',logout_view,name='logout'),
     path('register/',register,name='register'),
     path('available_books/',available_books,name='available_books'),
     path('rent/<int:book_id>/',rent_book,name='rent_book'),
     path('rental_success/<int:book_id>/<int:rental_id>/',rental_success, name='rental_success'),
     path('user_rentals/',user_rentals, name='user_rentals'),
     path('return_book/<int:rental_id>/',return_book, name='return_book'),
     path('manage_books/',manage_books, name='manage_books'),
     path('add_book/',add_book, name='add_book'),
     path('edit_book/<int:book_id>/',edit_book, name='edit_book'),
     path('delete_book/<int:book_id>/',delete_book, name='delete_book')
     
    
    
     
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)