from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Active_List, Bid, Category, User, Comment

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Active_List)
admin.site.register(Comment)
admin.site.register(Bid)