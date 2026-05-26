from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Patient, Slice, ActivityLog, PacsConfig, AuditLog
from .serializers import UserSerializer, PatientSerializer, SliceSerializer, ActivityLogSerializer, PacsConfigSerializer, AuditLogSerializer
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                first_name=data.get('name', '').split(' ')[0],
                last_name=' '.join(data.get('name', '').split(' ')[1:]),
                role=data.get('role', 'radiologist'),
                hospital=data.get('hospital', 'St. Luke Medical Center'),
                department=data.get('department', 'Radiology')
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')
        
        if not username or not new_password:
            return Response({'error': 'Username and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-id')
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class PacsConfigViewSet(viewsets.ModelViewSet):
    queryset = PacsConfig.objects.all()
    serializer_class = PacsConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all().order_by('-time')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
