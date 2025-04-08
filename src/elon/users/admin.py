from django.contrib import admin
from .models import User, Sms, Temp, Log


class userAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "firstname",  "lastname", "date_joined", "email")
    list_display_links = ('phone_number', 'email')
    search_fields = ['phone_number']


class smsAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code",  "created_datetime")
    list_display_links = ('phone_number', )
    search_fields = ['code','phone_number']

class TempAdmin(admin.ModelAdmin):
    list_display = ('phone_number','verified','verified_code')
    search_fields = ['phone_number','verified_code']

class LogAdmin(admin.ModelAdmin):
    list_display = ('user_id','messages','data')

admin.site.register(User, userAdmin)
admin.site.register(Sms, smsAdmin)
admin.site.register(Temp,TempAdmin)
admin.site.register(Log,LogAdmin)
