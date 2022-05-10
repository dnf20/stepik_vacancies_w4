from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from vacancies.models import Company, Vacancy, Specialty


class ApplicationForm(forms.Form):
    written_username = forms.CharField(max_length=64, label='Ваше имя')
    written_phone = forms.CharField(max_length=15, label='Ваш телефон')
    written_cover_letter = forms.CharField(max_length=5000, widget=forms.Textarea, label='Сопроводительное письмо')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить'))


class CompanyEditForm(forms.ModelForm):
    name = forms.CharField(
        max_length=64,
        label='Название компании',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyName',
                'type': 'text',
                }
        )
    )
    location = forms.CharField(
        max_length=64,
        label='География',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyLocation',
                'type': 'text'
                }
        )
    )
    logo = forms.FileField(
        label='Логотип',
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'inputGroupFile01',

            }
        )
    )
    description = forms.CharField(
        max_length=300,
        label='Информация о компании',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'companyInfo',
                'rows': '5',
                'style': 'color:#000;'
                }
        )
    )
    employee_count = forms.IntegerField(
        label='Количество человек в компании',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyTeam',
                }
        )
    )

    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count',)


class VacancyEditForm(forms.ModelForm):

    title = forms.CharField(
        max_length=64,
        label='Название вакансии',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'vacancyTitle',
                'type': 'text',
            }
        )
    )
    specialty = forms.ChoiceField(
        label='Специализация',
        widget=forms.Select(
            attrs={
                'class': 'custom-select mr-sm-2',
                'id': 'userSpecialization'
            }
        ),
        choices=((str(Specialty), str(Specialty)) for Specialty in Specialty.objects.all())
    )

    salary_min = forms.IntegerField(
        label='Зарплата от',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'vacancySalaryMin',
                }
        )
    )

    salary_max = forms.IntegerField(
        label='Зарплата до',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'vacancySalaryMax',
                }
        )
    )

    skills = forms.CharField(
        max_length=200,
        label='Требуемые навыки',
        widget=forms.Textarea(
            attrs={
                'rows': '3',
                'class': 'form-control',
                'id': 'vacancySkills',
                'style': "color:#000;"
            }
        )
    )

    description = forms.CharField(
        max_length=200,
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'rows': '15',
                'class': 'form-control',
                'id': 'vacancyDescription',
                'style': "color:#000;"
            }
        )
    )

    class Meta:
        model = Vacancy
        fields = ('title', 'salary_min', 'salary_max', 'skills', 'description', )
