from rest_framework import serializers
from .models import *


class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


