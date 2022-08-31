from django.urls import path
from events import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('events/', views.event_list),
    path('events/<int:pk>/', views.event_detail),
]


urlpatterns = format_suffix_patterns(urlpatterns)
