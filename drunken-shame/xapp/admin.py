from django.contrib import admin

from .models import tables


for model in tables:
    admin.site.register(model)
