from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('create-agency/', views.create_agency, name='create_agency'),
    path('send-invite/', views.send_invite, name='send_invite'),
]