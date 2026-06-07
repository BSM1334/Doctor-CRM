from django.contrib import admin
from django.urls import path, include



handler404 = 'webapp.views.custom_page_not_found_view'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('webapp.urls'))

]
