import re
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tài khoản có ký tự đặc biệt")
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("Tài khoản đã tồn tại")
        except User.DoesNotExist:
            return username

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
    
class ProfileForm(forms.ModelForm):
    
        avatar = forms.ImageField(required=False)
        
        class Meta:
            model = Profile
            fields = ['user', 'full_name' , 'address', 'phone_number', 'date_of_birth', 'university','avatar']
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()