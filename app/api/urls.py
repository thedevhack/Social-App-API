from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.ListUserView.as_view()),
    path("send_request/", views.CreateFriendRequest.as_view()),
    path("update_friend_request/", views.UpdateFriendRequest.as_view()),
    path("list_all_accepted_friends/", views.ListAllAcceptedFriends.as_view()),
    path("list_all_pending_friends/", views.ListAllPendingFriends.as_view()),
]
