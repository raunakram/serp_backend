
from django.urls import path
from .views import DataForSEOFetchAndSaveView, DataForSEOTaskPostView

urlpatterns = [
    path('dataforseo/regular/fetch/', DataForSEOFetchAndSaveView.as_view(), name='dataforseo-fetch-regular'),
    path('dataforseo/regular/task_post/for/post/method/', DataForSEOTaskPostView.as_view(), name='dataforseo-task-post'),
]