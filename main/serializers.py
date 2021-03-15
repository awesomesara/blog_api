from rest_framework import serializers
from.models import *
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    # updated_at = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)
    images = PostImageSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at', 'text', 'category', 'images')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
            fields.pop('images')
            fields.pop('text')
            fields.pop('created_at')
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comment'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        image_data = request.FILES
        # print(image_data)
        post = Post.objects.create(**validated_data)
        for image in image_data.getlist('images'):
            PostImage.objects.create(image=image, post=post)
            print(image)
        return post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        reply = Comment.objects.create(author=author, **validated_data)
        return reply

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['replies'] = CommentSerializer(instance.children.all(), many=True, context=self.context).data
        representation['author'] = instance.author.email
        return representation


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.author.email
        return representation


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        # representation['post'] =

        return representation
