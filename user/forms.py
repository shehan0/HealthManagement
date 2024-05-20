from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Dietitian, PracticeLocation
from user.models import User


class DietitianRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class DietitianForm(forms.ModelForm):
    class Meta:
        model = Dietitian
        fields = ['phone_number', 'country_of_practice']


class PracticeLocationForm(forms.ModelForm):
    class Meta:
        model = PracticeLocation
        fields = ['address', 'email', 'phone_number', 'website']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].required = True
        self.fields['address'].required = True

    def __str__(self):
        return (f"Address: {self.address}, "
                f"Email: {self.email}, "
                f"Phone Number: {self.phone_number}, "
                f"Website: {self.website}, ")
