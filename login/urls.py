
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from loginapp import views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('course/<str:subject>/', views.course, name='course'),
    path('record/<str:subject>/', views.record, name='record'),
    path('change-password/', views.change_password, name='change_password'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
