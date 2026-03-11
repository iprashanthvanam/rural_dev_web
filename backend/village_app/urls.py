

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('village_app.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('input/', views.input_form, name='input_form'),
#     path('success/<int:village_id>/', views.success, name='success'),
# ]




from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_form, name='input_form'),   # default page
    path('success/<int:village_id>/', views.success, name='success'),
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.input_form, name='input_form'),
#     path('home/', views.home, name='home'),
#     path('success/<int:village_id>/', views.success, name='success'),
# ]