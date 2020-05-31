from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email must be a valid email.")
        if len(postData['pw']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['pw'] != postData['confpw']:
            errors['conf_password'] = "Password & confirm password must match."
        return errors
    def validate_edit(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email must be a valid email.")
        return errors

class BookManager(models.Manager):
    def validate_quote(self, postData):
        errors = {}
        if len(postData['title']) < 0:
            errors["title"] = "Title is required."
        if len(postData['description']) < 5:
            errors["description"] = "Description should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name='favorited_book')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()