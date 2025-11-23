from rest_framework import serializers

from apps.common.models import NewsLetter


class NewsLetterSerializer(serializers.Serializer):
    class Meta:
        model = NewsLetter
        fields = ("email", )