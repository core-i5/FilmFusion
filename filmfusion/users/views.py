from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from .serializers import RegisterSerializer, UserSerializer
from django.utils.crypto import get_random_string
from django.utils import timezone
from .tasks import send_otp_email
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from filmfusion.permissions import IsAdminOrReadOnly
from filmfusion.authentication import UUIDJWTAuthentication
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        otp = get_random_string(length=6, allowed_chars='0123456789')
        send_otp_email.delay(email, otp)
        user = serializer.save(is_active=False)
        OTP.objects.create(user=user, otp=otp)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'detail': 'OTP sent to your email. Please verify.',
            'user': response.data
        }, status=status.HTTP_201_CREATED)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
            otp_record = OTP.objects.get(user=user)
            if otp_record.otp == otp and not otp_record.is_expired():
                user.is_active = True
                user.save()
                otp_record.delete()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'detail': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            otp_record, created = OTP.objects.get_or_create(user=user)
            otp_record.otp = otp
            otp_record.created_at = timezone.now()
            otp_record.save()
            send_otp_email.delay(email, otp)
            return Response({'detail': 'OTP sent to your email. Please verify.'})
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({'detail': 'User account is not active. Please verify your email.'}, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password != confirm_password:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            otp_record = OTP.objects.get(user=user)
            if otp_record.otp == otp and not otp_record.is_expired():
                user.set_password(new_password)
                user.save()
                otp_record.delete()
                return Response({'detail': 'Password updated successfully'})
            return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'detail': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [UUIDJWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [UUIDJWTAuthentication]
    pagination_class = StandardResultsSetPagination

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [UUIDJWTAuthentication]

    def get_object(self):
        try:
            user = self.request.user
            return user
      
        except Exception as e:
            logger.error(f'An error occurred: {str(e)}')
            return None