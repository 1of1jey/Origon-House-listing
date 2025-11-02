from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from origon.host_auth.models import CustomHost
from .serializers import (
    HostRegistrationSerializer, 
    HostLoginSerializer, 
    HostSerializer, 
    HostProfileSerializer,
    ChangeHostPasswordSerializer
)


class HostRegisterAPIView(generics.CreateAPIView):
    """
    API view for host registration
    """
    queryset = CustomHost.objects.all()
    serializer_class = HostRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            host = serializer.save()
            token, created = Token.objects.get_or_create(user=host)
            return Response({
                'message': 'Host registered successfully',
                'host': HostSerializer(host).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostLoginAPIView(APIView):
    """
    API view for host login
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = HostLoginSerializer(data=request.data)
        if serializer.is_valid():
            host = serializer.validated_data['host']
            if not host.is_active:
                return Response({'detail': 'Host account is disabled.'}, status=status.HTTP_403_FORBIDDEN)
            token, created = Token.objects.get_or_create(user=host)
            return Response({
                'message': 'Host login successful',
                'host': HostSerializer(host).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostLogoutAPIView(APIView):
    """
    API view for host logout
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Delete the host's token to logout
            request.user.auth_token.delete()
            return Response({
                'message': 'Host successfully logged out'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'error': 'Error logging out'
            }, status=status.HTTP_400_BAD_REQUEST)


class HostProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for getting and updating host profile
    """
    serializer_class = HostProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        host = self.get_object()
        serializer = HostSerializer(host)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeHostPasswordAPIView(APIView):
    """
    API view for changing host password
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangeHostPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            host = request.user
            host.set_password(serializer.validated_data['new_password'])
            host.save()
            # Delete all tokens to force re-login
            Token.objects.filter(user=host).delete()
            return Response({
                'message': 'Password changed successfully. Please login again.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def host_detail_view(request):
    """
    API view to get current host details
    """
    serializer = HostSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def host_verification_status(request):
    """
    API view to check host verification status
    """
    host = request.user
    return Response({
        'is_verified': host.is_verified,
        'verification_message': 'Verified host' if host.is_verified else 'Pending verification',
        'can_list_properties': host.is_verified and host.is_active
    }, status=status.HTTP_200_OK)