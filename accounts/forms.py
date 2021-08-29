from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from buyerseller.models import Category, Rfq
from .models import Profile
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img', 'organization', 'industry', 'address', 'city', 'state', 'country', 'zip',
                  'mobile',
                  'type', 'business_registeration_document', 'identity_document', 'business_owner', ]
        labels = {
            'business_owner': _('I am not the business owner'),
            'identity_document': _(
                'Upload your identity document so that we may verify you as a representative of your business. This could be your passport or any other officially issued identity document.'),
            'business_registeration_document': _(
                'Upload a copy of your business license, trade license, commercial register or other relevant business registration document. This lets us verify you as an official business. This can be a PDF, JPEG, TIF.'),
            'type': _('Account Type'),
        }


class BussinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'aboutus', 'bussiness_type', 'registration_number', 'location_of_registeration',
                  'business_registeration_document',
                  'products', 'otherproducts', 'year_of_company_registered', 'total_employees', 'website',
                  'company_advantage']
        labels = {
            'bussiness_type': _('Registered Business Type'),
            'bio': _('Brief Description About Organization'),
            'aboutus': _('ABOUT-US [section in webpage]'),
            'products': _('Main Products Name separated by commas '),
            'otherproducts': _('Other Products Names separated by commas '),
            'business_owner': _('I am not the business owner'),
            'identity_document': _(
                'Upload your identity document so that we may verify you as a representative of your business. This could be your passport or any other officially issued identity document.'),
            'business_registeration_document': _(
                'Upload a copy of your business license, trade license, commercial register or other relevant business registration document. This lets us verify you as an official business. This can be a PDF, JPEG, TIF.'),

        }


class CompanyImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img1', 'img2', 'img3']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class OrgUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['organization', 'industry', 'products', 'bio',
                  'type', 'business_registeration_document', 'identity_document', 'business_owner', ]
        labels = {
            'business_owner': _('I am not the business owner'),
            'identity_document': _(
                'Upload your identity document so that we may verify you as a representative of your business. This could be your passport or any other officially issued identity document.'),
            'business_registeration_document': _(
                'Upload a copy of your business license, trade license, commercial register or other relevant business registration document. This lets us verify you as an official business. This can be a PDF, JPEG, TIF.'),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('parent', 'title', 'slug', 'keywords', 'description', 'image', 'status', 'slug')
