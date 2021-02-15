import re
import datetime

from django import forms
from django.core.exceptions import ValidationError

from clients.models import City, Citizenship, Disability, MaritalStatus, Client


class ClientForm(forms.Form):
    last_name = forms.CharField(max_length=64,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=64,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(max_length=64,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    sex = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')),
                            widget=forms.widgets.RadioSelect())
    passport_serial = forms.CharField(max_length=2,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(max_length=6,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    passport_authority = forms.CharField(max_length=64,
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_issue_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    id_number = forms.CharField(max_length=64,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}),)
    birth_place = forms.CharField(max_length=64,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    living_place = forms.ModelChoiceField(queryset=City.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    living_address = forms.CharField(max_length=64,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    home_phone_number = forms.CharField(max_length=64, required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mobile_phone_number = forms.CharField(max_length=64, required=False,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=64, required=False,
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'required': False}))
    registration_place = forms.ModelChoiceField(queryset=City.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    marital_status = forms.ModelChoiceField(queryset=MaritalStatus.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    citizenship = forms.ModelChoiceField(queryset=Citizenship.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    disability = forms.ModelChoiceField(queryset=Disability.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    pensioner = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(attrs={'required': False}))
    monthly_income = forms.DecimalField(max_digits=19, decimal_places=4, required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        match = re.match(r'^[a-zA-Zа-яА-Я]+$', data)
        if match is None:
            raise ValidationError('Last name can only contain letters (a-zA-Z, а-яА-Я).')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        match = re.match(r'^[a-zA-Zа-яА-Я]+$', data)
        if match is None:
            raise ValidationError('First name can only contain letters (a-zA-Z, а-яА-Я).')
        return data

    def clean_middle_name(self):
        data = self.cleaned_data['middle_name']
        match = re.match(r'^[a-zA-Zа-яА-Я]+$', data)
        if match is None:
            raise ValidationError('Middle name can only contain letters (a-zA-Z, а-яА-Я).')
        return data

    def clean_passport_serial(self):
        data = self.cleaned_data['passport_serial']
        match = re.match(r'^[a-zA-Zа-яА-Я]+$', data)
        if match is None:
            raise ValidationError('Passport serial can only contain letters (a-zA-Z, а-яА-Я).')
        return data

    def clean_passport_number(self):
        data = self.cleaned_data['passport_number']
        data2 = self.cleaned_data['passport_serial']
        match = re.match(r'^[0-9]+$', data)
        if match is None:
            raise ValidationError('Passport number can only contain numbers (0-9).')
        if Client.objects.filter(passport_number=data, passport_serial=data2).exists():
            raise ValidationError('Client with this passport exists.')
        return data

    def clean_passport_authority(self):
        data = self.cleaned_data['passport_authority']
        match = re.match(r'^[a-zA-Zа-яА-Я0-9]+$', data)
        if match is None:
            raise ValidationError('Passport authority can only contain letters and numbers (a-zA-Z, а-яА-Я, 0-9).')
        return data

    def clean_id_number(self):
        data = self.cleaned_data['id_number']
        match = re.match(r'^[0-9]+$', data)
        if match is None:
            raise ValidationError('ID number can only contain numbers (0-9).')
        if Client.objects.filter(id_number=data).exists():
            raise ValidationError('Client with this id number exists.')
        return data

    def clean_birth_place(self):
        data = self.cleaned_data['birth_place']
        match = re.match(r'^[a-zA-Zа-яА-Я]+$', data)
        if match is None:
            raise ValidationError('Birth place can only contain letters (a-zA-Z, а-яА-Я).')
        return data

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        delta = (datetime.date.today()-data).days
        if delta < 0:
            raise ValidationError('Client cannot be from the future.')
        return data

    def clean_passport_issue_date(self):
        data = self.cleaned_data['passport_issue_date']
        delta = (datetime.date.today()-data).days
        if delta < 0:
            raise ValidationError('Client cannot be from the future.')
        return data


class DepositForm(forms.Form):
    last_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    passport = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    revocable = forms.ChoiceField(
        choices=((True, 'Revocable'), (False, 'Irrevocable')),
        widget=forms.RadioSelect()
    )
    number = forms.CharField(
        max_length=64,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    currency = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=19,
        decimal_places=4,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    percents = forms.DecimalField(
        max_digits=19,
        decimal_places=4,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


