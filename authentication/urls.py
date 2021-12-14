from .views import RegisterView, UsernameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView
from django.urls import path

#avoid django from checking for cross site request forgery on some some views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username' ),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-username'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate' ),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    
]