from django.contrib import admin
from .models import UserProf, Login, LoginOperational, LoginClient

admin.site.register(UserProf)
admin.site.register(Login)
admin.site.register(LoginOperational)
admin.site.register(LoginClient)

# Register your models here.
