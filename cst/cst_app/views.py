from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
import sqlite3, django, secrets, string
import django.conf as conf
# from django.db import connections
# from django.db.utils import DEFAULT_DB_ALIAS, load_backend
from cst.settings import BASE_DIR
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template 
from django.urls import reverse
from .utils import Utils
from django import db


@login_required(login_url='/login/')
def index_view(request):
    # print(conf.settings.DATABASES['primary'])
    # print(db.connections.databases)
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        # print(conf.settings.DATABASES['primary'])
        if user.role == 'Customer Standard User':
            customer = Customer.objects.get(email = email)
            agency = customer.agency_name.agency_name
            sqlite3.connect(f'{agency}.sqlite3')
            conf.settings.DATABASES['primary']['NAME'] = BASE_DIR / f'{agency}.sqlite3'
            print(conf.settings.DATABASES['primary'])
        return redirect('index_view')
    return render(request, 'login.html')

def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            user = request.user
            if user.role == 'Agency Admin':
                return redirect('create_agency')
            else:
                return redirect('index_view')
        else:
            print(form.errors)

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def create_agency(request):
    form = CreateAgency()
    if request.method == 'POST':
        form = CreateAgency(request.POST)
        if form.is_valid():
            user = request.user
            agency_form = form.save(commit=False)
            agency_form.created_by = user
            agency_form.agency_url = 'www.' + form.cleaned_data.get('agency_name') + '-agency.com'
            agency_form.save()
            name = agency_form.agency_name
            sqlite3.connect(f'{name}.sqlite3')
            conf.settings.DATABASES['primary']['NAME'] = BASE_DIR / f'{name}.sqlite3'
            print(conf.settings.DATABASES['primary'])
            django.core.management.execute_from_command_line(['manage.py', 'migrate', 'cst_app', '--database', 'primary'])
            return redirect('index_view')
        else:
            print(form.errors)
    return render(request, 'create_agency.html')

def send_invite(request):
    form = SendInvite()
    if request.method == 'POST':
        form = SendInvite(request.POST)
        if form.is_valid():
            agency = Agency.objects.get(id = 1)
            invite_form = form.save(commit=False)
            invite_form.password = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(7))
            invite_form.agency_name = agency
            invite_form.save()
            user = Customer.objects.get(email = invite_form.email)
            user.set_password(invite_form.password)
            user.save()
            current_site = get_current_site(request).domain
            relativeLink = reverse('login_view')
            absurl = 'http://'+ current_site + relativeLink
            context = {"user" : user.email, "absurl" : absurl, "password" : invite_form.password}
            email_body = get_template('email/send-invite.html').render(context)
            data = {'email_subject': 'Email PIN verification', 'email_body': email_body, 'to_email': user.email}
            Utils.send_email(data)
        else:
            print(form.errors)
    return render(request, 'send-invite.html', {"form": form})

# def create_connection(alias=DEFAULT_DB_ALIAS):
#     connections.ensure_defaults(alias)
#     connections.prepare_test_settings(alias)
#     db = connections.databases[alias]
#     backend = load_backend(db['ENGINE'])
#     return backend.DatabaseWrapper(db, alias)