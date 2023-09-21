from django.contrib import admin
from django.urls import path, include
from GLIMMA_AI import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='home'),
    path('', views.display_quiz, name='display_quiz'),  # This should handle the root URL
    path('quiz/', views.display_quiz, name='display_quiz'),  # This is redundant, you can remove it if you want
    path('', include("chat.urls")),  # Including the chat app URLs
    path('', include('GLIMMA_AI.urls')),
]

