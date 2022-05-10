import datetime

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import CASCADE, DO_NOTHING

from stepik_vacancies.settings import MEDIA_SPECIALTY_IMAGE_DIR, MEDIA_COMPANY_IMAGE_DIR


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    picture = models.ImageField(upload_to=MEDIA_SPECIALTY_IMAGE_DIR, height_field='height_field',
                                width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=DO_NOTHING, null=True, primary_key=False, related_name='owner_of')


class Vacancy(models.Model):
    title = models.CharField(max_length=256)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=CASCADE)
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(default=datetime.date.today)


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.CharField(max_length=100)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
