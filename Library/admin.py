from django.contrib import admin
from Library.models import Publisher, Author, Book, BookToAuthor, BookToPublisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	model = Publisher


@admin.register(Author)
class PublisherAdmin(admin.ModelAdmin):
	model = Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	model = Book


@admin.register(BookToPublisher)
class BookToPublisherAdmin(admin.ModelAdmin):
	model = BookToPublisher


@admin.register(BookToAuthor)
class BookToAuthorAdmin(admin.ModelAdmin):
	model = BookToAuthor
