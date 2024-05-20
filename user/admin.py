from django.contrib import admin

from user.models import User, Dietitian, PracticeLocation

# Register your models here.

admin.site.register(User)
admin.site.register(Dietitian)
admin.site.register(PracticeLocation)