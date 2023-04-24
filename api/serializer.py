from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    topic = serializers.CharField()
    content = serializers.CharField()
    image_url = serializers.CharField()
