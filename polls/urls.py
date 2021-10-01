from django.urls import path

from . import views


app_name = "polls"
urlpatterns = [
  path('', views.index, name="index"),
  path('<int:question_id>/detail/', views.detail, name="questionDetail"),
  path('<int:question_id>/vote/', views.vote, name="vote"),
  path('<int:question_id>/result/', views.result, name="result"),
  path('hello', views.hello)
]