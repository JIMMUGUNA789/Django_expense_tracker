from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth

# Create your views here.
class RegisterView(View):
    #handle a get request
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        #TODO register user


        #? get user data
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        #?validate user data
        context ={
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<8:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                activate_url = 'https://'+domain+link



                email_subject = 'Activate Your Account'
                email_body = 'Hi' + user.username + 'Please verify your account via this link' + activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'mugunajim@gmail.com',
                    [email],
                    # ['bcc@example.com'],
                    # reply_to=['example@c.com'],
                    # headers={'Message-ID':'foo'}
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account created successfully')



        #?create user 
        return render(request, 'authentication/register.html', context)

class UsernameValidationView(View):
    #handle a get request
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        #check if username contains alphanumerics only
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should contain alphanumerics only'}, status=400 )#bad request
            #check if user exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username already exists, choose another one'}, status=409 )#conflicting resource
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    #handle a get request
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        #check if username contains alphanumerics only
        if not validate_email(email):
            return JsonResponse({'email_error':'Invalid Email'}, status=400 )#bad request
            #check if user exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email already exists, choose another one'}, status=409 )#conflicting resource
        return JsonResponse({'email_valid': True})

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)
            #checkif user has not activated before
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
            





        except Exception as ex:
            pass
        return redirect('login')

class LoginView(View):  
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, '+ user.username + ' You are now logged in')
                    return redirect('expenses')
                messages.error(request, 'Account not active. Please checkyour email')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid Credentials. Please try again')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Logged out sucessfully')
        return redirect('login')

        