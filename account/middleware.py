from datetime import date
from django.utils.deprecation import MiddlewareMixin
from .models import TrafficData

class TrafficMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Exclude admin and static files from tracking
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return

        today = date.today()
        traffic, created = TrafficData.objects.get_or_create(date=today)
        
        # Increase visit count
        traffic.total_visits += 1
        
        # Track unique visitors by session
        if not request.session.get('has_visited_today'):
            traffic.unique_visitors += 1
            request.session['has_visited_today'] = True

        traffic.save()
