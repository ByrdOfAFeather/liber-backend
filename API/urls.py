from django.contrib import admin
from django.urls import path, include
from API import views

app_name = "api"
urlpatterns = [
	path('publisher', views.PublisherEndpoint.as_view(), name="publisher"),   # Used for publisher pagination
	# path('publisher/<int:publisher_id>', views.publishers, name="publisher"),    # Used for action on a single publisher
	# path('search', name="search"),
]
