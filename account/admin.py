from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import TrafficData, Profile

# Admin for Profile model
class ProfileAdmin(UnfoldModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)

# Admin for TrafficData model
@admin.register(TrafficData)
class TrafficDataAdmin(UnfoldModelAdmin):
    list_display = ('date', 'total_visits', 'unique_visitors')
    list_filter = ('date',)

# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = "past year question"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('traffic/', self.admin_view(self.traffic_dashboard)),
        ]
        return custom_urls + urls

    def traffic_dashboard(self, request):
        traffic_data = TrafficData.objects.all().order_by('-date')[:7]

        dates = [data.date.strftime('%Y-%m-%d') for data in traffic_data]
        total_visits = [data.total_visits for data in traffic_data]
        unique_visitors = [data.unique_visitors for data in traffic_data]

        context = {
            "dates": dates,
            "total_visits": total_visits,
            "unique_visitors": unique_visitors,
        }
        return render(request, 'admin/traffic_dashboard.html', context)

# Instantiate the custom admin site
admin_site = CustomAdminSite(name='custom_admin')
