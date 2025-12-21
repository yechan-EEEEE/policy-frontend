from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'birth_date', 'region', 'job', 'gender', 'profile_image']
        read_only_fields=['id']
        
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='비밀번호 확인')
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'real_name', 'birth_date', 'region', 'job', 'gender']
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            real_name=validated_data['real_name'],
            birth_date=validated_data['birth_date'],
            region=validated_data['region'],
            job=validated_data['job'],
            gender=validated_data['gender'],     
        )
        return user
    
class UserDetailSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = User
        fields = [
        
            'id', 'username', 'real_name', 'birth_date', 'region',
            'job', 'gender', 'posts_count', 'comments_count', 'date_joined'
            
        ]
        read_only_fields = ['id', 'date_joined']