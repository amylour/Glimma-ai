from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('quiz/', views.display_quiz, name='display_quiz'),
    path('save_answer/', views.save_answer, name='save_answer'),
]
