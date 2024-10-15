from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Message, Blog  

# Custom admin for Message model using UnfoldModelAdmin
class MessageAdmin(UnfoldModelAdmin):
    pass  # Add customizations if needed

# Custom admin for Blog model using UnfoldModelAdmin
class BlogAdmin(UnfoldModelAdmin):
    pass  # Add customizations if needed

# Register your models with the customized UnfoldModelAdmin
admin.site.register(Message, MessageAdmin)
admin.site.register(Blog, BlogAdmin)