from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    print(request.POST)
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hashed_password)
    print(new_user, "New user has been registered!")
    request.session['name'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/books')

def login(request):
    logged_user = User.objects.filter(email = request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            print(logged_user, "Logged user has been signed in!")
            request.session['name'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/books')
    return redirect('/')

def logout(request):
    logout = request.session.clear()
    print(logout, "User has logged out.")
    return redirect('/')

def books(request):
    context = {
        'all_books': Book.objects.all()
    }
    return render(request, 'books.html', context)

def add(request):
    if request.method == 'POST':
        errors = Book.objects.validate_quote(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        new_book = Book.objects.create(title = request.POST['title'], description = request.POST['description'], poster = User.objects.get(id = request.session['id']))
        print(new_book, "New book has been posted!")
        return redirect('/books')
    return redirect('/')

def favorite(request, book_id):
    user_favorite = User.objects.get(id = request.session['id'])
    favorited_book = Book.objects.get(id = book_id)
    favorited_book.favorite.add(user_favorite)
    return redirect('/books')

def destroy(request, book_id):
    one_book = Book.objects.get(id = book_id)
    if one_book.poster.id == request.session['id']:
        one_book.delete()
    return redirect('/books')