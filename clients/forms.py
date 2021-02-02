from django import forms

from clients.models import City, Citizenship, Disability, MaritalStatus, Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%d-%m-%Y', attrs={'type':'date', 'class': 'form-control'}),
            'sex': forms.RadioSelect(),
            'passport_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'passport_authority': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_issue_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date', 'class': 'form-control'}),
            'id_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'living_place': forms.Select(attrs={'class': 'form-control'}),
            'living_address': forms.TextInput(attrs={'class': 'form-control'}),
            'home_phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
            'mobile_phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'registration_place': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'citizenship': forms.Select(attrs={'class': 'form-control'}),
            'disability': forms.Select(attrs={'class': 'form-control'}),
            'pensioner': forms.CheckboxInput(attrs={'required': False}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control', 'required': False})
        }
    '''last_name = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    middle_name = forms.CharField(max_length=64)
    birth_date = forms.DateField()
    sex = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')), widget=forms.widgets.RadioSelect)
    passport_serial = forms.CharField(max_length=64)
    passport_number = forms.CharField(max_length=64)
    passport_authority = forms.CharField(max_length=64)
    passport_issue_date = forms.DateField()
    id_number = forms.CharField(max_length=64)
    birth_place = forms.CharField(max_length=64)
    living_place = forms.ModelChoiceField(queryset=City.objects.all())
    living_address = forms.CharField(max_length=64)
    home_phone_number = forms.CharField(max_length=64, required=False)
    mobile_phone_number = forms.CharField(max_length=64, required=False)
    email = forms.CharField(max_length=64, required=False)
    registration_place = forms.ModelChoiceField(queryset=City.objects.all())
    marital_status = forms.ModelChoiceField(queryset=MaritalStatus.objects.all())
    citizenship = forms.ModelChoiceField(queryset=Citizenship.objects.all())
    disability = forms.ModelChoiceField(queryset=Disability.objects.all())
    pensioner = forms.BooleanField(required=False)
    monthly_income = forms.DecimalField(max_digits=19, decimal_places=4, required=False)'''