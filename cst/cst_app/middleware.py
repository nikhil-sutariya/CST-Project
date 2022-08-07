from django.utils.deprecation import MiddlewareMixin
from .models import Customer
import threading

tenant_thread = threading.local()

class RouterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            user = request.user
            if user.role == 'Customer Standard User':
                customer = Customer.objects.get(email = user.email)
                agency = customer.agency_name.agency_name
                tenant_thread.agency = agency

    def process_response(self, request, response):
        if hasattr(tenant_thread, 'agency'):
            del tenant_thread.agency
        return response
