from django.contrib import admin
from django.urls import path
from django.conf.urls import  url,include
from . import views
app_name='querypage'

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('querypage/',include('querypage.urls'))
    path('landing/',views.landing,name='landing'),
    path('keyword/',views.keyword,name='keyword'),
    path('filter/',views.filter,name='filter'),
]
 