from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name="all-profiles-views"),
    path('<slug>/', views.ProfileDetialsView.as_view(), name="profile-detail"),
    path('myprofile/', views.my_profile_view, name="my-profile"),
    path('myinvites/', views.invites_received_view, name="my-invites"),
    path('to-invite/', views.invite_profiles_list_view, name="invite-profiles"),
    path('sent-invite/', views.send_invitation, name="send-invite"),
    path('remove-invite/', views.remove_from_friends, name="remove-invite"),
    path('accept-invite/', views.accept_inv, name="accept-invite"),
    path('reject-invite/', views.reject_inv, name="reject-invite" ),
]
