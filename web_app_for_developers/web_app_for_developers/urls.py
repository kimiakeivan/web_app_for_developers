from django.urls import path,include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/' , include('project.urls')),
    path('' , include('users.urls')),
    path('api/' , include('api.urls'))
]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)