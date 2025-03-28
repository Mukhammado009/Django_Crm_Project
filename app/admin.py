from django.contrib import admin
from .models import CustomUser, Client,Task
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Task)