from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/global_admin/', admin.site.urls),
    path('', include(('profile_user.urls'))),
    path('client/', include(('client.urls'))),
    path('inventory/', include(('inventory.urls'))),
    path('service/', include(('service.urls'))),
    path('administrator/', include(('administrator.urls'))),
    path('booking/', include(('booking.urls'))),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
