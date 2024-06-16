from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bms_app.urls')),


    path('accounts/', include('allauth.urls'),name='provider_login_url'),

    path('social/', include('social_django.urls', namespace='social'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)