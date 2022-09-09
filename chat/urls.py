from django.urls import path
from chat import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('messages/<uuid:pk>/', views.EventMessagesList.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
