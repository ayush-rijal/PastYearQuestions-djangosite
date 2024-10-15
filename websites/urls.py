from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('slider/', views.slider_list, name='slider'),
    path('chat-tai/', views.chatbot, name='chatbot'),  # Correct view reference here
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
