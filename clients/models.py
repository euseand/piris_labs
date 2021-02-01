from django.db import models
from django.urls import reverse_lazy


class City(models.Model):
    city_name = models.CharField(max_length=64)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class MaritalStatus(models.Model):
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Statuses'


class Citizenship(models.Model):
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'Citizenship'
        verbose_name_plural = 'Citizenships'


class Disability(models.Model):
    type = models.CharField(max_length=64)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'


class Client(models.Model):
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    passport_serial = models.CharField(max_length=64)
    passport_number = models.CharField(max_length=64)
    passport_authority = models.CharField(max_length=64)
    passport_issue_date = models.DateField()
    id_number = models.CharField(max_length=64)
    birth_place = models.CharField(max_length=64)
    living_place = models.ForeignKey(City, related_name='clients_living_place', on_delete=models.RESTRICT)
    living_address = models.CharField(max_length=64)
    home_phone_number = models.CharField(max_length=64, blank=True)
    mobile_phone_number = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    registration_place = models.ForeignKey(City, related_name='clients_registration_place', on_delete=models.RESTRICT)
    marital_status = models.ForeignKey(MaritalStatus, related_name='clients_martial_status', on_delete=models.RESTRICT)
    citizenship = models.ForeignKey(Citizenship, related_name='clients_citizenship', on_delete=models.RESTRICT)
    disability = models.ForeignKey(Disability, related_name='clients_disability', on_delete=models.RESTRICT)
    pensioner = models.BooleanField(choices=((True, 'Yes'), (False, 'No')))
    monthly_income = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.last_name + self.first_name

    def get_absolute_url(self):
        return reverse_lazy('client', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'







