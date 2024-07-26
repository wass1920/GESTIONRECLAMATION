from django.contrib import admin
from .models import Operateur, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email' , 'password')
admin.site.register(User, UserAdmin)

class OperateurAdmin(admin.ModelAdmin):
    list_display = ('name', 'email' , 'numtel','password')

admin.site.register(Operateur, OperateurAdmin)


