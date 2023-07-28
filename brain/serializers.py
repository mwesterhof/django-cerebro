from rest_framework import serializers

from .models import VisitorBehavior


class VisitorBehaviorSerializer(serializers.Serializer):
    time_spent = serializers.IntegerField()
    pages_visited = serializers.IntegerField()

    conversion_target_a = serializers.IntegerField()
    conversion_target_b = serializers.IntegerField()

    def create(self, validated_data):
        return VisitorBehavior.objects.create(**validated_data)


class VisitorBehaviorSerializerForPrediction(serializers.Serializer):
    time_spent = serializers.IntegerField()
    pages_visited = serializers.IntegerField()

    conversion_target_a = serializers.IntegerField(read_only=True)
    conversion_target_b = serializers.IntegerField(read_only=True)
