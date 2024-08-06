from django.urls import path
from .views import *

urlpatterns = [
    # Onboarding
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('retrieve_update_destroy/', UserRetrieveUpdateDestroyView.as_view(), name='user_retrieve_update_destroy'),
    path('retrieve_update_destroy/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user_retrieve_update_destroy'),
    ]
