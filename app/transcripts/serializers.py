from typing import List

from rest_framework import serializers


class TranscriptionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    text = serializers.CharField()
    folder = serializers.CharField(max_length=255)
    topics = serializers.ListField(child=serializers.CharField(max_length=100), allow_empty=True)
    length_sec = serializers.IntegerField(min_value=0)
    speakers = serializers.ListField(child=serializers.CharField(max_length=100), allow_empty=True)


class TranscriptionUpdateSerializer(TranscriptionSerializer):
    pass
