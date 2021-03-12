from rest_framework import serializers
from.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    # updated = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at', 'text', 'category')

    # def get_fields(self):
    #     action = self.context.get('action')
    #     fields = super().get_fields()
    #     if action == 'list':
    #         fields.pop('images')
    #         fields.pop('description')
    #         fields.pop('created')
    #     return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comment'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        return representation

    def create(self, validate_data):
        request = self.context.get('request')
        user_id = request.user.id
        validate_data['author_id'] = user_id
        post = Post.objects.create(**validate_data)
        return post


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


# class RecursiveSerializer(serializers.Serializer):
#
#     def to_representation(self, instance):
#         serializer = self.parent.parent.__class__(instance, context=self.context)
#         return serializer.data
#
#
# class FilterCommentListSerializer(serializers.ListSerializer):
#
#     def to_representation(self, data):
#         data = data.filter(parent=None)
#         return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # children = RecursiveSerializer(many=True)

    class Meta:
        # list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        reply = Comment.objects.create(author=author, **validated_data)
        return reply