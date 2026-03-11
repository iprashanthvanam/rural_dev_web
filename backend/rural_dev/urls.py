

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static



# from django.views.static import serve
# from django.urls import re_path
# import os
# from django.conf import settings


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('village_app.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# OUTPUT_DIR = os.path.join(settings.BASE_DIR, "outputs")

# urlpatterns += [
#     re_path(r'^outputs/(?P<path>.*)$', serve, {'document_root': OUTPUT_DIR}),
# ]










from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
import os

OUTPUT_DIR = os.path.join(settings.BASE_DIR, "outputs")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('village_app.urls')),
]

urlpatterns += [
    re_path(r'^outputs/(?P<path>.*)$', serve, {'document_root': OUTPUT_DIR}),
]