from django.urls import path
from .views import *

# Defining URLs for the app.
urlpatterns = [
    path('chat', chat, name='chat'),
    path('ajax/', Ajax, name='ajax'),
]
