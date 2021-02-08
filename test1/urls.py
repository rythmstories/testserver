from django.contrib import admin
from django.conf.urls import url, include
# from django.conf.urls.static import static
# from django.conf import setttings

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'view/', include('server1.urls')),
]

