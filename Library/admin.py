from django.contrib import admin
from Library.models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	model = Publisher
