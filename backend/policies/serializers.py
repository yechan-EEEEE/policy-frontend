from rest_framework import serializers
from .models import Policy

class PolicySerializer(serializers.ModelSerializer):
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Policy
        fields = '__all__'
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False
    
class PolicyListSerializer(serializers.ModelSerializer):
    
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    
    class Meta:
        model = Policy
        fields = ['plcyNo', 'plcyNm', 'plcyExplnCn', 'lclsfNm', 'mclsfNm', 
                  'sprvsnInstCdNm', 'plcyKywdNm', 'liked_count']
    
class PolicyDetailSerializer(serializers.ModelSerializer):
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Policy
        fields = '__all__'
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False