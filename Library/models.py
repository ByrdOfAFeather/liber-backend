from django.db import models

COVER_CHOICES = [
	("HARDBACK", "Hardback"),
	("SOFTBACK", "Softback"),
	("MASSMARKETPAPERBACK", "Softback"),
	("LIBRARYBINDING", "Softback"),
	("SPIRALBINDING", "Softback"),
	("LEATHERBINDING", "Softback"),
	("TURTLEBACK", "Softback"),
]


class Publisher(models.Model):
	name = models.TextField(unique=True)


class Book(models.Model):
	title = models.TextField()
	publish_date = models.DateField()
	publisher = models.ForeignKey(Publisher, blank=True, on_delete=models.CASCADE)
	edition = None
	volume = None
	spine_type = models.CharField(max_length=19, choices=COVER_CHOICES, default="HARDBACK")
	isbn_number = models.CharField(max_length=13, blank=True)  # Blank if the book was published before 1970
	favorite = models.BooleanField(default=False)


class Author(models.Model):
	name = models.CharField(max_length=58)  # TODO: This perhaps could be longer
	nationality = None  # TODO: What type should this be? Perhaps a custom location, perhaps not. Flags should exist
	bio = None  # TODO: Perhaps this shouldn't be included at all
	olid = models.TextField(null=True, unique=True)  # TODO: This is probably a fixed length


class BookToAuthor(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
