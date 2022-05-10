"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, AllVacanciesView, VacancyView, CompanyView, custom_handler404, \
    custom_handler500, SpecialtyVacanciesView, MyRegisterView, MyLogoutView, MyLoginView, vacancy_apply_view, \
    MyCompanyView, MyCompanyCreateView, MyCompanyVacancyEditView, MyCompanyVacanciesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
    path('vacancies/', AllVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_code>/', SpecialtyVacanciesView.as_view(), name='specialty_vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', vacancy_apply_view, name='application'),
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/create/', MyCompanyCreateView.as_view()),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>', MyCompanyVacancyEditView.as_view()),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', MyRegisterView.as_view(), name='register'),
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
