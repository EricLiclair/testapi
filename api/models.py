from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import string
import random
# Create your models here.


def generate_unique_id() -> str:
    length: int = 9
    while True:
        id: str = ''.join(random.choices(string.ascii_uppercase, k=length))
        try:
            if Profile.objects.filter(id=id).count() == 0:
                break
        except:
            return id
    return id


class Profile(models.Model):
    class Institutes(models.TextChoices):
        IIITRANCHI = 'IIITRANCHI', _(
            'Indian Institute of Information Technology Ranchi')
        INSTI_A = 'INSTI_A', _('Institute A')
        INSTI_B = 'INSTI_B', _('Institute B')
        INSTI_C = 'INSTI_C', _('Institute C')
        INSTI_D = 'INSTI_D', _('Institute D')
        OTHER = 'OTHER', _('Other Institute')

    class Branch(models.TextChoices):
        CSE_UG = 'CSE_UG', _(
            'Computer Science and Engineering (Undergraduate)')
        ECE_UG = 'ECE_UG', _(
            'Electronics and Communications Engineering (Undergraduate)')

    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')

    class Language(models.TextChoices):
        PYTHON = 'PY', _('Python')
        CPP = 'CPP', _('C++')
        C = 'C', _('C')
        JAVA = 'JAVA', _('Java')

    id = models.CharField(
        primary_key=True,
        default=generate_unique_id,
        editable=False,
        unique=True,
        max_length=16
    )

    institute = models.CharField(
        _('institute name'),
        choices=Institutes.choices,
        default=Institutes.IIITRANCHI,
        max_length=100,
    )

    branch = models.CharField(
        _('branch'),
        choices=Branch.choices,
        default=Branch.CSE_UG,
        max_length=100,
    )

    year = models.CharField(
        _('year'),
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
        max_length=2,
    )

    github_url = models.URLField(
        _('github url'),
        max_length=255,
        null=True,
    )

    primary_language = models.CharField(
        _('primary programming language'),
        choices=Language.choices,
        default=Language.PYTHON,
        max_length=5,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.user.get_username()
