from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Policy
from .serializers import PolicySerializer, PolicyListSerializer, PolicyDetailSerializer
import requests
from django.conf import settings
from datetime import datetime
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def policy_list(request):
    policies = Policy.objects.all()
    
    # 검색어 필터
    search  = request.query_params.get('search', None)
    if search:
        policies = policies.filter(plcyNm__icontains=search)
        
    # 지역 필터
    region = request.query_params.get('region', None)
    if region:
        policies = policies.filter(sprvsnInstCdNm__icontains=region)
        
    # 대분류 필터
    category = request.query_params.get('category', None)
    if category:
        policies = policies.filter(lclsfNm=category)
        
    serializer = PolicyListSerializer(policies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def policy_detail(request, plcyNo):
    policy = get_object_or_404(Policy, plcyNo=plcyNo)
    serializer = PolicyDetailSerializer(policy, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def policy_like(request, plcyNo):
    policy = get_object_or_404(Policy, plcyNo=plcyNo)
    user = request.user
    
    if policy.liked_users.filter(id=user.id).exists():
        policy.liked_users.remove(user)
        return Response(
            {'message': '좋아요가 취소되었습니다', 'is_liked': False},
            status=status.HTTP_200_OK
        )
    else:
        policy.liked_users.add(user)
        return Response(
            {'message': '좋아요가 추가되었습니다', 'is_likes': True},
            status=status.HTTP_201_CREATED
        )
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def policy_recommend(request):
    user = request.user
    
    today = datetime.today()
    user_age = today.year - user.birth_date.year
    
    policies = Policy.objects.filter(
        sprvsnInstCdNm__icontains=user.region
    ).filter(
        sprtTrgtMinAge__lte=user_age,
        sprtTrgtMaxAge__gte=user_age
    )
    
    # policies = policies.annotate(
    #     like_count=models.Count('liked_users')
    # ).order_by('-like_count')[:10]
    
    serializer = PolicyListSerializer(policies, many=True)
    return Response(serializer.data)