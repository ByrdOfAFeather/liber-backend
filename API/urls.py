from django.contrib import admin
from django.urls import path, include
from API import views

app_name = "api"
urlpatterns = [
	path('publisher', views.PublisherEndpoint.as_view(), name="publisher"),
	path('author', views.AuthorEndpoint.as_view(), name="author"),
	path('book', views.BookEndpoint.as_view(), name="book"),
]
