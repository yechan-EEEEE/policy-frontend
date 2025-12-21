from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    REGION_CHOICES = [
        ('서울특별시', '서울특별시'),
        ('부산광역시', '부산광역시'),
        ('대구광역시', '대구광역시'),
        ('인천광역시', '인천광역시'),
        ('광주광역시', '광주광역시'),
        ('대전광역시', '대전광역시'),
        ('울산광역시', '울산광역시'),
        ('세종특별자치시', '세종특별자치시'),
        ('경기도', '경기도'),
        ('강원특별자치도', '강원특별자치도'),
        ('충청북도', '충청북도'),
        ('충청남도', '충청남도'),
        ('전북특별자치도', '전북특별자치도'),
        ('전라남도', '전라남도'),
        ('경상북도', '경상북도'),
        ('경상남도', '경상남도'),
        ('제주특별자치도', '제주특별자치도'),
    ]

    real_name = models.CharField(max_length=50, blank=True,verbose_name="이름")
    birth_date = models.DateField(null=True, blank=True,verbose_name="생년월일")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True, blank=True,verbose_name="지역")
    job = models.CharField(max_length=50, null=True, blank=True,verbose_name="직업")
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICES, verbose_name="성별")
    
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )
    
    def __str__(self):
        return self.username