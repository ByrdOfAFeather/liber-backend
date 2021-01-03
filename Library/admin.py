from django.contrib import admin
from Library.models import Publisher, Author


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	model = Publisher


@admin.register(Author)
class PublisherAdmin(admin.ModelAdmin):
	model = Author
