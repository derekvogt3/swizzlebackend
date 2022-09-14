from django.urls import path
from events import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('events/', views.event_list),
    path('events/<uuid:pk>/', views.event_detail),
    path('events/public/<uuid:pk>/', views.PublicEventDetail.as_view()),
    path('invitation/', views.InvitationList.as_view()),
    path('events/messages/', views.event_messages_list)
]


urlpatterns = format_suffix_patterns(urlpatterns)
