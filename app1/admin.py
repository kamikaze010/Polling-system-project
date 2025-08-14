from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,PollOptions,Poll,Profile
# from .models import Category, CategoryItem






class CustomUserAdmin(UserAdmin):
    list_display = ('username','first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(CustomUser,CustomUserAdmin)




class PollAdmin(admin.ModelAdmin):
    list_display =[ 'id','question']
admin.site.register(Poll,PollAdmin) 

class PollOptionsAdmin(admin.ModelAdmin):
    list_display = ['id','poll','option_text','votes']
admin.site.register(PollOptions,PollOptionsAdmin)