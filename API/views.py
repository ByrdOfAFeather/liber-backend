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
from Library.models import Publisher, Author


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
		if pagination_index := request.query_params.get("pagination_index", ""):
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
		elif name := request.query_params.get("name", ""):
			if name:
				try:
					valid_objects = self.related_model.objects.get(
						name=name
					)
					return Response(self.jsonify_model(valid_objects), status=200)
				except self.related_model.DoesNotExist:
					return Response({
						"error": "No object found",
					}, status=404)
			else:
				return Response({"error": "Must specify name to search by"}, status=400)
		else:
			return Response({"error": "Bad request"}, status=400)

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
		return {
			"name": model_instance.name,
			# "nationality": model_instance.nationality,
			# "bio": model_instance.bio,
			"id": model_instance.id
		}

	def get(self, request, format=None):
		return super(AuthorEndpoint, self).get(request, format=format)

	def post(self, request, format=None):
		return super(AuthorEndpoint, self).post(request, format=format)

