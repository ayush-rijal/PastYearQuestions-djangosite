from django import forms
from .models import Slider
from .models import Chat
from django.contrib import admin    
from unfold.admin import ModelAdmin as UnfoldModelAdmin

class SliderAdmin(UnfoldModelAdmin):
    pass
    class Meta:
        model = Slider
        fields = ['name', 'logo']

admin.site.register(Slider, SliderAdmin )


class ChatAdmin(UnfoldModelAdmin):
    pass

# Register your models here.
admin.site.register(Chat)