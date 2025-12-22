from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Policy
from .serializers import PolicySerializer, PolicyListSerializer, PolicyDetailSerializer
import requests
import google.generativeai as genai
from django.conf import settings
from django.db import models
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
    
    policies = policies.annotate(
        like_count=models.Count('liked_users')
    ).order_by('-like_count')[:10]
    
    serializer = PolicyListSerializer(policies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def fetch_policies(request):
    api_key = settings.YOUTH_API_KEY
    base_url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
    
    page_num = 1
    page_size = 100  # 한 번에 100개씩
    total_saved = 0
    
    try:
        while True:
            params = {
                'apiKeyNm': api_key,
                'pageNum': page_num,
                'pageSize': page_size,
                'rtnType': 'json'
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('resultCode') != 200:
                break
            
            policy_list = data.get('result', {}).get('youthPolicyList', [])
            
            if not policy_list:
                break
            
            # 데이터 저장
            for policy_data in policy_list:
                Policy.objects.update_or_create(
                    plcyNo=policy_data['plcyNo'],
                    defaults={
                        'plcyNm': policy_data.get('plcyNm', ''),
                        'plcyExplnCn': policy_data.get('plcyExplnCn', ''),
                        'lclsfNm': policy_data.get('lclsfNm', ''),
                        'mclsfNm': policy_data.get('mclsfNm', ''),
                        'plcyKywdNm': policy_data.get('plcyKywdNm', ''),
                        'plcySprtCn': policy_data.get('plcySprtCn', ''),
                        'sprvsnInstCdNm': policy_data.get('sprvsnInstCdNm', ''),
                        'sprtTrgtMinAge': int(policy_data.get('sprtTrgtMinAge') or 0) if policy_data.get('sprtTrgtMinAge') else 0,
                        'sprtTrgtMaxAge': int(policy_data.get('sprtTrgtMaxAge') or 999) if policy_data.get('sprtTrgtMaxAge') else 999,
                        'bizPrdBgngYmd': policy_data.get('bizPrdBgngYmd', ''),
                        'bizPrdEndYmd': policy_data.get('bizPrdEndYmd', ''),
                        'jobCd': policy_data.get('jobCd', ''),
                        'schoolCd': policy_data.get('schoolCd', ''),
                        'aplyUrlAddr': policy_data.get('aplyUrlAddr', ''),
                        'refUrlAddr1': policy_data.get('refUrlAddr1', ''),
                    }
                )
                total_saved += 1
            
            page_num += 1
        
        return Response(
            {'message': f'{total_saved}개의 정책 데이터를 저장했습니다.'},
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['POST'])
@permission_classes([AllowAny])
def policy_summarize(request, plcyNo):
    policy = get_object_or_404(Policy, plcyNo=plcyNo)
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
            다음 청년 정책을 3-5줄로 요약해주세요. 반드시 아래 형식을 따라주세요:

            **정책명**: {policy.plcyNm}

            **지원 내용**:
            {policy.plcySprtCn}

            **상세 설명**:
            {policy.plcyExplnCn}

            요약 시 다음 내용을 포함해주세요:
            1. 핵심 지원 내용 (한 줄)
            2. 신청 자격 요건 (한 줄)  
            3. 주요 혜택 (한 줄)

            간단명료하게 작성해주세요.
        """
        response = model.generate_content(prompt)
        summary = response.text
        
        return Response({
            'plcyNo': plcyNo,
            'plcyNm': policy.plcyNm,
            'summary': summary
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'요약 생성 중 오류가 발생했습니다: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )