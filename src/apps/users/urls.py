from django.urls import path
from .views import UserListView
from rest_framework.routers import SimpleRouter

app_name = 'router'
router = SimpleRouter()

urlpatterns = [
    path('', UserListView.as_view(), name='all_users_list')
]
