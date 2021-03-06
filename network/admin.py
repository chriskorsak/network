from django.contrib import admin

from . models import User, Post

class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "first_name", "last_name", "email", "id")

class PostAdmin(admin.ModelAdmin):
  list_display = ("creator", "date")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
