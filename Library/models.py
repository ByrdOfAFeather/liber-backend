from django.db import models

COVER_CHOICES = [
	("HARDCOVER", "Hardcover"),
	("SOFTCOVER", "Softcover"),
	("MASSMARKETPAPERBACK", "Mass Market Paperback"),
	("LIBRARYBINDING", "Library Binding"),
	("SPIRALBINDING", "Spiral Binding"),
	("LEATHERBOUND", "Leather Bound"),
	("TURTLEBACK", "Turtleback"),
	("UNKNOWN", "Unknown")
]


class Publisher(models.Model):
	name = models.TextField(unique=True)


class Book(models.Model):
	title = models.TextField()
	publish_date = models.CharField(max_length=200)
	edition = None
	volume = None
	spine_type = models.CharField(max_length=19, choices=COVER_CHOICES, default="HARDBACK")
	isbn_number = models.CharField(max_length=13, blank=True, unique=True)  # Blank if the book was published before 1970
	favorite = models.BooleanField(default=False)

	def __str__(self):
		return self.title


class Author(models.Model):
	name = models.CharField(max_length=58)  # TODO: This perhaps could be longer
	nationality = None  # TODO: What type should this be? Perhaps a custom location, perhaps not. Flags should exist
	bio = None  # TODO: Perhaps this shouldn't be included at all
	olid = models.TextField(null=True, unique=True)  # TODO: This is probably a fixed length

	def __str__(self):
		return self.name


class BookToAuthor(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	list_display = ("book", "author")


class BookToPublisher(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	list_display = ("book", "publisher")
