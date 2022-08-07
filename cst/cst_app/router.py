from django.conf import settings
from cst_app.middleware import tenant_thread

class DataBaseRouter(object):
    # def _default_db(self):
    #     if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
    #         return 'primary'
    #     else:
    #         return 'default'
            
    # def db_for_read(self, model, **hints):
    #     if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
    #         print(tenant_thread.agency)
    #         return 'primary'
    #     else:
    #         return 'default'

    # def db_for_write( self, model, **hints ):
    #     if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
    #         print(tenant_thread.agency)
    #         return 'primary'
    #     else:
    #         return 'default'

        #####

    def db_for_read(self, model, **hints):
        if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
            return 'primary'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
            return 'primary'
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if hasattr(tenant_thread, 'agency') and tenant_thread.agency in settings.DATABASES:
            return 'primary'
        else:
            return 'default'