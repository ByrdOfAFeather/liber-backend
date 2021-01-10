from Library.models import COVER_CHOICES
from rest_framework import serializers


class BookSearlizer(serializers.Serializer):
	authors = serializers.ListField(allow_empty=True, allow_null=False)
	publishers = serializers.ListField(allow_empty=True, allow_null=False)
	isbn = serializers.CharField(max_length=13, min_length=10, allow_blank=True, allow_null=False)
	title = serializers.CharField(max_length=1000, allow_blank=False, allow_null=False)
	physical_format = serializers.ChoiceField(choices=COVER_CHOICES)
	publish_date = serializers.CharField()
