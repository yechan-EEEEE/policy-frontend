from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Post, Comment
from django.db.models import Count
from .serializers import (
    PostListSerializer, PostSerializer, PostDetailSerializer,
    CommentSerializer
)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def thread_list(request):
    if request.method == 'GET':
        posts = Post.objects.annotate(
            like_count=Count('liked_users', distinct=True),
            comment_count=Count('comments', distinct=True),
        )

        # 🔍 검색
        search = request.query_params.get('search')
        if search:
            posts = posts.filter(title__icontains=search)

        # 🔥 정렬
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering == 'popular':
            posts = posts.order_by('-like_count', '-created_at')
        else:
            posts = posts.order_by('-created_at')

        serializer = PostListSerializer(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def thread_detail(request, thread_pk):
    post = get_object_or_404(Post, pk=thread_pk)
    
    if request.method == 'GET':
        post.view_count += 1
        post.save()
        
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if post.author != request.user:
            return Response(
                {'error': '수정 권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if post.author != request.user:
            return Response(
                {'error': '삭제 권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.delete()
        return Response(
            {'message': '게시글이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    
    if post.liked_users.filter(id=user.id).exists():
        post.liked_users.remove(user)
        liked = False
    else:
        post.liked_users.add(user)
        liked = True

    return Response(
        {
            'is_liked': liked,
            'liked_count': post.liked_users.count(),
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def thread_list_by_policy(request, plcyNo):
    posts = Post.objects.filter(policy__plcyNo=plcyNo).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def comment_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'GET':
        comments = post.comments.all()
        
        popular_comments = comments.annotate(
            like_count=models.Count('liked_users')
        ).filter(like_count__gte=3).order_by('-like_count')
        
        normal_comments = comments.annotate(
            like_count=models.Count('liked_users')
        ).filter(like_count__lt=3).order_by('-created_at')
        
        all_comments = list(popular_comments) + list(normal_comments)
        
        serializer = CommentSerializer(all_comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if not request.user.is_authenticated:
        return Response(
            {'error': '로그인이 필요합니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if comment.author != request.user:
        return Response(
            {'error': '권한이 없습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(
            {'message': '댓글이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    
    if comment.liked_users.filter(id=user.id).exists():
        comment.liked_users.remove(user)
        return Response(
            {'message': '좋아요가 취소되었습니다.', 'is_liked': False},
            status=status.HTTP_200_OK
        )
    else:
        comment.liked_users.add(user)
        return Response(
            {'message': '좋아요가 추가되었습니다.', 'is_liked': True},
            status=status.HTTP_201_CREATED
        )