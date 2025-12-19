from django.db import models
from django.conf import settings

# Create your models here.
class Policy(models.Model):
    
    # 정책 기본 정보
    plcyNo = models.CharField(max_length=100, unique=True, primary_key=True, verbose_name='정책번호')
    plcyNm =models.CharField(max_length=200, verbose_name="정책명")
    plcyExplnCn = models.TextField(verbose_name="정책설명")
    
    # 분류
    lclsfNm = models.CharField(max_length=50, verbose_name="대분류")
    mclsfNm = models.CharField(max_length=50, verbose_name="중분류")
    plcyKywdNm = models.CharField(max_length=100, blank=True, null=True, verbose_name="키워드")
    
    # 지원 내용
    plcySprtCn = models.TextField(verbose_name="지원내용")
    
    # 지역 및 기관
    sprvsnInstCdNm = models.CharField(max_length=100, verbose_name="지역")
    
    # 나이 제한
    sprtTrgtMinAge = models.IntegerField(default=0, verbose_name="최소나이")
    sprtTrgtMaxAge = models.IntegerField(default=0, verbose_name="최대나이")
    
    # 사업 기간
    bizPrdBgngYmd = models.CharField(max_length=8, blank=True, verbose_name="사업시작일")
    bizPrdEndYmd = models.CharField(max_length=8, blank=True, verbose_name="사업종료일")
    
    # 직업/학력
    jobCd = models.CharField(max_length=200, blank=True, verbose_name="직업코드")
    schoolCd = models.CharField(max_length=50, blank=True, verbose_name="학력코드")
        
    # URL
    aplyUrlAddr = models.URLField(max_length=500, blank=True, verbose_name="신청URL")
    refUrlAddr1 = models.URLField(max_length=500, blank=True, verbose_name="참고URL")
    
    # 좋아요
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_policies',
        blank=True, 
    )
    
    class Meta:
        ordering = ['-plcyNo']
        
    def __str__(self):
        return self.plcyNm