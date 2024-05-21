from django import forms
from .models import UserProfile, Product, Cart

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ="__all__"

        
# Other forms...

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password']

class UserProfileForm(forms.ModelForm):
   
    class Meta:
        model = UserProfile
        fields = [ 'username','first_name', 'last_name', 'email','profile_picture']
   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']
