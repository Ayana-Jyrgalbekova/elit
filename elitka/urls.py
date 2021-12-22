from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.views import *
from elitka import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homes/', HomeList.as_view(), name='homes'),
    path('detail/<int:pk>/', Detail.as_view(), name='detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user'),
    path('report/<int:my_id>/', create_report, name='report'),
    path('ipoteka/', ipoteka, name='ipoteka'),
    path('create/', add_home, name='create'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('map/', test, name='test'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
