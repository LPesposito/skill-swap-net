from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("feed/", views.feed_view, name="feed_alias"),
    path("requests/", views.MyRequestsListView.as_view(), name="requests"),
    path("offers/", views.MyOffersListView.as_view(), name="offers"),
    path("requests/new/", views.ServiceRequestCreateView.as_view(), name="request_create"),
    path("requests/<int:pk>/status/", views.update_request_status, name="request_status"),
]
