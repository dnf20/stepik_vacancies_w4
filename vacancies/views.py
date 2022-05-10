from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView

from vacancies.forms import ApplicationForm, CompanyEditForm, VacancyEditForm
from vacancies.models import Specialty, Company, Vacancy, Application


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class AllVacanciesView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecialtyVacanciesView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(SpecialtyVacanciesView, self).get_context_data(**kwargs)
        specialty_code = kwargs['specialty_code']
        try:
            specialty = Specialty.objects.get(code=specialty_code)
        except Specialty.DoesNotExist:
            raise Http404(f"specialty code='{specialty_code}' not found")
        vacancies = Vacancy.objects.filter(specialty__code=specialty_code)
        context['specialty'] = specialty
        context['vacancies'] = vacancies
        return context


class CompanyView(TemplateView):
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = int(self.kwargs['company_id'])
        try:
            context['company'] = Company.objects.get(id=company_id)
            context['vacancies'] = Vacancy.objects.filter(company__id=company_id)
        except Company.DoesNotExist:
            raise Http404(f"company id {company_id} not found")
        return context


class VacancyView(TemplateView):
    template_name = "vacancy.html"

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = int(self.kwargs['vacancy_id'])
        try:
            context['vacancy'] = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404(f"vacancy id={vacancy_id} not found")
        return context


class MyLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    template_name = "logout.html"


class MyRegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = "/login"


def vacancy_apply_view(request, vacancy_id: int):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        raise Http404(f"vacancy id {vacancy_id} not found")
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            data = application_form.cleaned_data
            Application(
                written_username=data['written_username'],
                written_phone=data['written_phone'],
                written_cover_letter=data['written_cover_letter'],
                vacancy=vacancy,
                user=request.user
            ).save()
            return HttpResponseRedirect('/')
        else:
            raise Http404
    else:
        application_form = ApplicationForm()
    return render(request, 'vacancy-application.html', {'form': application_form})


class MyCompanyCreateView(View):
    template_name = 'company-create.html'

    def get(self, request):
        return render(
            request, self.template_name, context={}
        )

    def post(self, request):
        Company.objects.create(
            name='Введите название компании',
            location='Введите местоположение компании',
            description='Введите описание компании',
            employee_count=1,
            logo=None,
            owner=request.user
        )
        return redirect('/mycompany/')


class MyCompanyView(View):
    template_name = 'company-edit.html'
    updated = False

    def get(self, request):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if request.method == 'GET':
            form = CompanyEditForm(instance=company)
        else:
            form = CompanyEditForm(request.POST, request.FILES, instance=company)
        if company is None:
            return redirect('/mycompany/create/')
        return render(
            request, self.template_name,
            context={
                'form': form,
                'company': company,
                'updated': self.updated
            }
        )

    def post(self, request):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if request.method == 'GET':
            form = CompanyEditForm(instance=company)
        else:
            form = CompanyEditForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            self.updated = True
            return redirect('/mycompany/')
        else:
            form = CompanyEditForm(instance=company)
        return render(
            request, self.template_name,
            context={
                'form': form,
                'company': company,
                'updated': self.updated
            })


class MyCompanyVacanciesView(LoginView):
    template_name = 'vacancy-list.html'

    def get(self, request, **kwargs):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if company is None:
            return redirect('/mycompany/create/')
        vacancies = Vacancy.objects.filter(company=company).all()
        return render(
            request, self.template_name,
            context={
                'vacancies': vacancies
            }
        )


class MyCompanyVacancyEditView(LoginView):
    template_name = 'vacancy-edit.html'
    updated = False

    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if vacancy:
            form = VacancyEditForm(instance=vacancy)
        else:
            specialty = Specialty.objects.all().first()
            vacancy = Vacancy.objects.create(
                title='Введите название вакансии',
                company=company,
                skills='Введите требуемые навыки',
                description='Введите описание',
                salary_min=0,
                salary_max=0,
                specialty=specialty
            )
            form = VacancyEditForm(instance=vacancy)
        applications = Application.objects.filter(vacancy=vacancy).all()
        return render(
            request, self.template_name,
            context={
                'applications': applications,
                'company': company,
                'form': form,
                'updated': self.updated,
                'vacancy': vacancy
            }
        )

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        user = request.user
        company = Company.objects.filter(owner=user).first()
        form = VacancyEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            specialty = Specialty.objects.filter(title=request.POST['specialty']).first()
            post_form = form.save(commit=False)
            post_form.specialty = specialty
            post_form.company = company
            post_form.save()
            self.updated = True
        else:
            form = VacancyEditForm(instance=vacancy)
        applications = Application.objects.filter(vacancy=vacancy).all()
        return render(
            request, self.template_name,
            context={
                'applications': applications,
                'company': company,
                'form': form,
                'updated': self.updated,
                'vacancy': vacancy,
            }
        )


def custom_handler404(request, exception):
    return render(request, 'page404.html', context={'exception': exception})


def custom_handler500(request):
    return render(request, 'page500.html', status=500)
