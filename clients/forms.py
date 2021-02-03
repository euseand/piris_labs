from django import forms

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
    passport_serial = forms.CharField(max_length=64,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(max_length=64,
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
