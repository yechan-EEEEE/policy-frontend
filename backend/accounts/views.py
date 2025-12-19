from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer, UserDetailSerializer
# Create your views here.

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
        
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': '아이디와 비밀번호를 입력해주세요'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )   
    else:
        return Response(
            {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response(
        {'message': '로그아웃 되었습니다'},
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request):
    user = request.user
    user.delete()
    return Response(
        {'messsage': '회원 탈퇴가 완료되었습니다.'},
        status=status.HTTP_204_NO_CONTENT
    )