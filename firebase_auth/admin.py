from django.contrib import admin
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)
