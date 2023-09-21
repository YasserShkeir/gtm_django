from rest_framework import serializers
from .models import Content, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        exclude = ["id", "language"]

class DashBoardRowSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='language.name')
    class Meta:
        model = Content
        fields = "__all__"