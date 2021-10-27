from rest_framework import serializers

from .models import News, Feed, SourceForParse


class GetNewsSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=200, allow_null=True)
    pub_date = serializers.CharField(max_length=200, allow_blank=True)
    limit = serializers.IntegerField(min_value=0, allow_null=True)
    json = serializers.BooleanField(default=True)
    to_pdf = serializers.BooleanField(default=False)
    to_json = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return validated_data


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = "__all__"


class SourceForParseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceForParse
        fields = "__all__"
