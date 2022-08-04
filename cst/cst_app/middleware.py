from django.utils.deprecation import MiddlewareMixin
import threading
from django.conf import settings
from .models import Customer

tenant_thread = threading.local()

# class RouterMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, args, kwargs):
#         user = request.user
#         # return user

#     def process_response(self, request, response):
#         return response

# class DataBaseRouter(object):
#     def db_for_read(self, model, user_id=None, **hints):
#         # a = self.process_view()
#         # print(a)
#         if user_id == 3:
#             print(user_id)
#             return "primary"
#         return "default"

#     def db_for_write(self, model, user_id=None, **hints):
#         # a = self.process_view()
#         if user_id == 3:
#             return "primary"
#         return "default"

class RouterMiddleware(MiddlewareMixin):
    def process_view( self, request, view_func, args, kwargs ):
        user = request.user
        if user.role == 'Customer Standard User':
            customer = Customer.objects.get(email = user.email)
            agency = customer.agency_name.agency_name
            
            tenant_thread.cfg = agency

        return None

    def process_response(self, request, response):
        if hasattr(tenant_thread, 'cfg'):
            del tenant_thread.cfg
        return response

class DataBaseRouter(object):
    def _default_db(self):
        if hasattr(tenant_thread, 'cfg') and tenant_thread.cfg in settings.DATABASES:
            print(tenant_thread.cfg)
            return tenant_thread.cfg
        else:
            return 'default'
            
    def db_for_read( self, model, **hints ):
        return self._default_db()

    def db_for_write( self, model, **hints ):
        return self._default_db()