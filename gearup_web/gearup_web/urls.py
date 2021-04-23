"""gearup_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.views.decorators.cache import cache_page
from webapp.views import HomePageView, CustomPageView, DisabilityAccessView, NCCollegesView,\
    CareersView, CollegeDetailView, CareerDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='HOME'),
    path('disability-access/', DisabilityAccessView.as_view(), name='DISABILITY_ACCESS'),
    path('colleges/', NCCollegesView.as_view(), name='NC_COLLEGES'),
    path('careers/', CareersView.as_view(), name='CAREERS'),
    path('pages/<uuid:page_uid>/', CustomPageView.as_view(),
         name='custom-page'),
    path('colleges/<uuid:college_uid>/', CollegeDetailView.as_view(),
         name='college_detail'),
    path('careers/<uuid:career_uid>/', CareerDetailView.as_view(),
         name='career_detail'),
]
