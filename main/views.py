from datetime import timedelta, datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .permissions import IsPostAuthor
from .serializers import PostImageSerializer, CategorySerializer, PostSerializer, CommentSerializer, RatingSerializer, \
    LikeSerializer, FavouriteSerializer, HistorySerializer, ParsSerializer
from .utils import add_post
from .pars import main


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsPostAuthor, ]
        elif self.action == 'get':
            permissions = [AllowAny, ]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]

    @action(detail=False, methods=['get'])
    def category(self, request):
        queryset = Post.objects.all()
        queryset = queryset.filter(category=request.category)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet, PermissionMixin):
    queryset = Post.objects.all()
    queryset_fav = Favourite.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user, post=post,)
        if not created:
            obj.is_active = not obj.is_active
            obj.save()
        liked_or_unliked = 'liked' if obj.is_active else 'unliked'

        return Response('Successfully {} post!'.format(liked_or_unliked), status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favourite(self, request, pk=None):
        post = self.get_object()
        obj, created = Favourite.objects.get_or_create(user=request.user, post=post, )
        if not created:
            obj.favourite = not obj.favourite
            obj.save()
        favourites = 'added to favorites' if obj.favourite else 'removed to favorites'

        return Response('Successfully {} !'.format(favourites), status=status.HTTP_200_OK)

    #filter
    @action(detail=False, methods=['get'])
    def own(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def favourites(self, request):
        queryset = Favourite.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavouriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user = request.user
        add_post(instance, user)
        return Response(serializer.data)


class PostImageViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class CommentViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class LikeAPIView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.get(pk=post_id).likes.all()
        return queryset


class HistoryAPIView(APIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        post = History.objects.filter(user=user)
        serializer = HistorySerializer(instance=post, many=True).data
        return Response(serializer)


class ParsAPIView(APIView):

    def get(self, request):
        dict_ = main()
        serializer = ParsSerializer(instance=dict_, many=True)
        return Response(serializer.data)

