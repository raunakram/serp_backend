from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('get_post_data_app.urls')),
    path('api/user/', include('user.urls')),
]
