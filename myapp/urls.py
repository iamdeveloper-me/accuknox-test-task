from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('user-search/', UserSearchView.as_view(), name='user-search'),
    path('send-request/', SendRequestView.as_view(),
         name='send-request'),
    path('respond-to-request/<int:friend_request_id>/',
         RespondToRequestView.as_view(), name='respond-to-friend-request'),
    path('accepted-request-list/', AcceptedRequestListView.as_view(), name='accepted-request-list'),
    path('pending-request-list/', PendingRequestsView.as_view(),name ='pending-request-list')
]
