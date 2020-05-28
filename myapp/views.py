from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
from myapp.forms import SignUpForm, SignInForm
from myapp.models import PUser, Tournament
from myapp.tasks import some_task, exact_time_run
from myapp.utils import token_generator


def index(request):
    form = SignUpForm()
    login_form = SignInForm()
    user_count = User.objects.filter(is_active=True).count()
    tournaments = Tournament.objects.all().order_by('-created_at')
    p_user = ''
    # exact_time_run.apply_async(eta=datetime.datetime(2020, 5, 26, 0, 15))
    if not request.user.is_anonymous:
        p_user = PUser.objects.filter(user=request.user).get()
    return render(request, 'myapp/index.html',
                  {'form': form, 'login_form': login_form, 'user_count': user_count,
                   'tournaments': tournaments, 'p_user': p_user})


def signup(request):
    form = SignUpForm()
    login_form = SignInForm()
    user_count = User.objects.filter(is_active=True).count()
    tournaments = Tournament.objects.all().order_by('-created_at')
    p_user = ''
    if not request.user.is_anonymous:
        p_user = PUser.objects.filter(user=request.user).get()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            PUser.objects.create(user=user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            domain = get_current_site(request).domain
            activate_url = 'http://' + domain + '/activate/' + uidb64 + '/' + token_generator.make_token(user)
            subject = 'Activate your account'
            message = 'Hi ' + user.username + '\nPlease use this link to verify your account\n' + activate_url
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

    return render(request, 'myapp/index.html',
                  {'form': form, 'login_form': login_form, 'user_count': user_count,
                   'tournaments': tournaments, 'p_user': p_user})


def login_user(request):
    form = SignUpForm()
    login_form = SignInForm()
    user_count = User.objects.filter(is_active=True).count()
    tournaments = Tournament.objects.all().order_by('-created_at')
    p_user = ''
    if request.method == 'POST':
        login_form = SignInForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            p_user = PUser.objects.filter(user=user).get()
        if login_form.is_valid() and user:
            login(request, user)
            return render(request, 'myapp/index.html',
                          {'form': form, 'login_form': login_form, 'user_count': user_count,
                           'tournaments': tournaments, 'p_user': p_user})
    return render(request, 'myapp/index.html',
                  {'form': form, 'login_form': login_form, 'user_count': user_count,
                   'tournaments': tournaments, 'p_user': p_user})


def logout_user(request):
    logout(request)
    return redirect('index')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        p_user = PUser.objects.get(user=user)
        p_user.email_verified_at = timezone.now()
        p_user.save()
        user.save()
        login(request, user)
    return redirect('index')


def add_tournament(request, id):
    tournament = Tournament.objects.get(id=id)
    user = PUser.objects.filter(user=request.user).first()
    # Tournament.objects.filter(p_user=user)
    tournament.p_user.add(user)
    tournament.save()
    return redirect('index')
