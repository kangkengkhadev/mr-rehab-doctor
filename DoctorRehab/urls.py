"""rehabtesting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as views
import patientinfo.views as pviews
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.login_page),
    path('register/', views.signup_page),
    path('login/', views.login_page),
    path('postsignUp/',views.postsignUp),
    path('postsignIn/',views.postsignIn),
    path('addpatientdata/',views.patientdata),
    path('addpatientcase/',views.addpatientcase),
    path('doctorpage/',views.doctorpage),
    path('deld/',views.del_dsession),
    path('selectpose/',views.selectpose),
    path('patientinfo/',pviews.patientpage),
    path('patientinfo/<pid>/',pviews.patientpage),
    path('changepose/',pviews.changepose),
    path('savechangepose/',pviews.savechangepose),
    path('changepatientinfo/',pviews.changepatientinfo),
    path('savechangepinfo/',pviews.savechangepinfo),
]
