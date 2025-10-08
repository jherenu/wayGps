from rest_framework import serializers
from .models import Movil


class MovilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movil
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')