from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    Claiming_Client = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'list': 'existing-clients',
            'placeholder': 'Select or enter client name'
        })
    )
    Claimed_Amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'})
    )

    class Meta:
        model = Shipment
        fields = '__all__'  # Include all fields from Shipment model
        widgets = {
            'Claim_No': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'Claiming_Client': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'Branch': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'Intend_Claim_Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'Formal_Claim_Date_Received': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Closed_Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Amount_Paid_By_Carrier': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'Amount_Paid_By_Awa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'Amount_Paid_By_Insurance': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'Formal_Claim_Received': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super(ShipmentForm, self).__init__(*args, **kwargs)

    def clean_Claim_No(self):
        Claim_No = self.cleaned_data.get('Claim_No')
        if not Claim_No.startswith('S'):
            raise ValidationError("Claim number must start with 'S'.")
        if Shipment.objects.filter(Claim_No=Claim_No).exclude(id=self.instance.id if self.instance else None).exists():
            raise ValidationError("This claim number already exists. Please enter a unique number.")
        return Claim_No

    def clean(self):
        cleaned_data = super().clean()
        # Ensure required fields are provided
        if not cleaned_data.get('Claiming_Client'):
            self.add_error('Claiming_Client', 'This field is required.')
        if not cleaned_data.get('Branch'):
            self.add_error('Branch', 'This field is required.')
        if not cleaned_data.get('Intend_Claim_Date'):
            self.add_error('Intend_Claim_Date', 'This field is required.')
        return cleaned_data

# User management forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
