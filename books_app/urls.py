from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
    path('add_book', views.add),
    path('favorite/<int:book_id>', views.favorite),
    path('delete/<int:book_id>', views.destroy),

]
