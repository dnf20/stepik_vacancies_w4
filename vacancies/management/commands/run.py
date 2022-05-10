import datetime

from django.core.management import BaseCommand

from vacancies.data import companies, specialties, jobs
from vacancies.models import Company, Specialty, Vacancy


class Command(BaseCommand):

    def handle(self, *args, **options):
        for company in companies:
            Company.objects.create(
                id=int(company['id']),
                name=company['title'],
                logo=company['logo'],
                employee_count=int(company['employee_count']),
                location=company['location'],
                description=company['description'],
            )
            # c = Company.objects.get(id=int(company['id']))
            # c.logo = company['logo']
            # c.save()
        for specialty in specialties:
            # s = Specialty.objects.get(code=specialty['code'])
            # s.picture = specialty['picture']
            # s.save()
            Specialty.objects.create(
                code=specialty['code'],
                title=specialty['title'],
                picture=specialty['picture'],
            )
        for job in jobs:
            job_id = int(job['id'])
            title = job['title']
            salary_from = int(job['salary_from'])
            salary_to = int(job['salary_to'])
            skills = job['skills']
            specialty = Specialty.objects.filter(code=job['specialty']).first()
            company = Company.objects.filter(id=int(job['company'])).first()
            published_at = datetime.datetime.strptime(job['posted'], '%Y-%m-%d').date()
            description = job['description']
            Vacancy(
                id=job_id,
                title=title,
                specialty=specialty,
                company=company,
                salary_min=salary_from,
                salary_max=salary_to,
                skills=skills,
                published_at=published_at,
                description=description
            ).save()
