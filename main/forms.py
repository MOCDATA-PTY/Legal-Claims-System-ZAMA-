from django import forms
from django.core.exceptions import ValidationError
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'  # Ensures all fields in the model are included in the form
        widgets = {
            'Intend_Claim_Date': forms.DateInput(attrs={'type': 'date'}),
            'Formal_Claim_Date_Received': forms.DateInput(attrs={'type': 'date'}),
            'Closed_Date': forms.DateInput(attrs={'type': 'date'}),
            'Claimed_Amount': forms.NumberInput(attrs={'step': '0.01'}),
            'Amount_Paid_By_Carrier': forms.NumberInput(attrs={'step': '0.01'}),
            'Amount_Paid_By_Awa': forms.NumberInput(attrs={'step': '0.01'}),
            'Amount_Paid_By_Insurance': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_Claim_No(self):
        Claim_No = self.cleaned_data.get('Claim_No')
        if not Claim_No.startswith('S'):
            raise ValidationError("Shipment number must start with 'S'.")

        # Check for duplicate Claim_No
        if Shipment.objects.filter(Claim_No=Claim_No).exists():
            raise ValidationError("This claim number already exists. Please enter a unique number.")

        return Claim_No

    def clean(self):
        cleaned_data = super().clean()
        Formal_Claim_Received = cleaned_data.get('Formal_Claim_Received')
        Formal_Claim_Date_Received = cleaned_data.get('Formal_Claim_Date_Received')

        if Formal_Claim_Received == 'NO' and Formal_Claim_Date_Received:
            cleaned_data['Formal_Claim_Date_Received'] = None  # Clear the date if 'NO' is selected
        return cleaned_data


# Additional forms for user management
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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
