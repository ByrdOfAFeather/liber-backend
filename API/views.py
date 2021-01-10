from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from Library.models import Publisher, Author, Book, BookToAuthor, BookToPublisher
import io
from rest_framework.parsers import JSONParser

from API.seralizers import BookSearlizer


@api_view(["POST"])
def books():
	pass


class NamedEntityEndpoint(APIView):
	"""
	"""

	def __init__(self):
		self.related_model = None  # Subclasses change this
		super(NamedEntityEndpoint, self).__init__()

	def jsonify_model(self, model_instance):
		"""
		Returns a jsonified version of the model, implemented by subclasses
		"""
		raise NotImplementedError

	def get(self, request, format=None):
		if pagination_index := request.query_params.get("pagination_index", False):
			end_of_pagination = False
			try:
				pagination_index = int(pagination_index)
			except ValueError:
				return Response({"error": "pagination_index must be integer"}, status=400)
			all_objects = self.related_model.objects.order_by("name")
			if len(all_objects) <= pagination_index + 10:
				end_of_pagination = True

			paginated_objects = [self.jsonify_model(i) for i in all_objects[pagination_index: pagination_index + 10]]
			return Response({"result": paginated_objects, "end_of_pagination": end_of_pagination},
			                status=200)
		elif name := request.query_params.get("name", False):
			"""
			Searches the database for an exact match first. If this is found, the resulting response will indicate 
			that there is an exact match in the first index. Then the database is search for .startswith. this will 
			consist of the rest of the list. If nothing is found a 404 will be returned, if anything is found a 200 
			will be returned along with the objects found. 
			"""
			exact_match = None
			try:
				exact_match = self.jsonify_model(self.related_model.objects.get(
					name=name
				))
			except self.related_model.DoesNotExist:
				exact_match = None
			valid_objects = []
			if exact_match:
				valid_objects.append(exact_match)
			valid_objects.extend(
				[self.jsonify_model(obj) for obj in self.related_model.objects.filter(
					name__startswith=name
				)]
			)
			if valid_objects:
				return Response({"results": valid_objects, "exact_match": exact_match is not None}, status=200)
			else:
				return Response({"error": "No objects found", "exact_match": False}, status=404)
		elif olid := request.query_params.get("olid", False):
			try:
				found_object = self.related_model.objects.get(
					olid=olid
				)
				return Response({"results": self.jsonify_model(found_object), "exact_match": True}, status=200)
			except self.related_model.DoesNotExist:
				return Response({"error": "Could not find a model", "exact_match": True}, status=404)
		else:
			return Response({"error": "Bad request", "exact_match": False}, status=400)

	def post(self, request, format=None):
		name = request.data.get("name", "")
		if name:
			try:
				new_object = self.related_model.objects.create(
					name=name
				)
				return Response(self.jsonify_model(new_object), status=200)
			except IntegrityError:
				return Response({
					"error": "An object with this name already exists"
				}, status=403)
		else:
			return Response({
				"error": "Must provide a name"
			}, status=403)


class PublisherEndpoint(NamedEntityEndpoint):
	def __init__(self):
		super(PublisherEndpoint, self).__init__()
		self.related_model = Publisher

	def jsonify_model(self, model_instance):
		return {
			"name": model_instance.name,
			"id": model_instance.id
		}

	def get(self, request, format=None):
		return super(PublisherEndpoint, self).get(request, format=format)

	def post(self, request, format=None):
		return super(PublisherEndpoint, self).post(request, format=format)


class AuthorEndpoint(NamedEntityEndpoint):
	def __init__(self):
		super(AuthorEndpoint, self).__init__()
		self.related_model = Author

	def jsonify_model(self, model_instance):
		"""Note that id here is OLID, not the database id as is the case with publishers
		"""
		return {
			"name": model_instance.name,
			# "nationality": model_instance.nationality,
			# "bio": model_instance.bio,
			"id": model_instance.olid
		}

	def get(self, request, format=None):
		return super(AuthorEndpoint, self).get(request, format=format)

	def post(self, request, format=None):
		name = request.data.get("name", "")
		olid = request.data.get("olid", None)
		if name and olid:
			try:
				new_object = self.related_model.objects.create(
					name=name,
					olid=olid
				)
				return Response(self.jsonify_model(new_object), status=200)
			except IntegrityError:
				return Response({
					"error": "An object with this name already exists"
				}, status=403)
		else:
			return Response({
				"error": "Must provide a name"
			}, status=403)


class BookEndpoint(APIView):
	def post(self, request, format=None):
		seralizer = BookSearlizer(data=request.data)
		if seralizer.is_valid():
			try:
				new_book = Book.objects.create(
					title=seralizer.data.get("title"),
					isbn_number=seralizer.data.get("isbn"),
					publish_date=seralizer.data.get("publish_date"),
					spine_type=seralizer.data.get("physical_format"),
				)
				for author_data in seralizer.data.get("authors"):
					author = None
					try:
						author = Author.objects.get(
							olid=author_data["id"]
						)
					except Author.DoesNotExist:
						author = Author.objects.create(
							name=author_data["name"],
							olid=author_data["id"]
						)
					BookToAuthor.objects.create(
						book=new_book,
						author=author
					)
				for publisher_data in seralizer.data.get("publishers"):
					publisher = None
					try:
						publisher = Publisher.objects.get(
							id=publisher_data["id"]
						)
					except Publisher.DoesNotExist:
						publisher = Publisher.objects.create(
							name=publisher_data["name"],
							id=publisher_data["id"]
						)
					BookToPublisher.objects.create(
						book=new_book,
						publisher=publisher
					)
				return Response(
					{"success": "book created."},
					status=200
				)
			except IntegrityError as e:
				return Response({"error": "Book already exists"}, status=403)
		else:
			return Response(
				seralizer.errors,
				status=403
			)
