from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Chat
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     reply = Chat.objects.create(user=user, **validated_data)
    #     return reply

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['replies'] = CommentSerializer(instance.children.all(), many=True, context=self.context).data
        representation['user'] = instance.user.email
        return representation
