from django.urls import path
from .views import profile_view

app_name = 'profiles'

urlpatterns = [
    path('', profile_view, name='profile-view'),
    # path('sleep/', test_view_1, name='test-view-1'),
    # path('view3/', test_view_2, name='test-view-2'),
]
