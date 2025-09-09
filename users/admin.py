from django.contrib import admin
from .models import User
# Register your models here.A
admin.site.site_header = "MTS Admin"
admin.site.site_title = "MTS Admin Portal"
admin.site.index_title = "Welcome to MTS Admin Portal"

admin.site.register(User)