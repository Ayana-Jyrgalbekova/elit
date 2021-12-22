from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from core.models import NewUser, Home, Photo, Report, ReportImage


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'text')


class HomeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Home
        fields = ('title', 'description', 'city', 'region', 'street',
                  'price', 'meter', 'class_home', 'floor', 'materials',
                  'height', 'company', 'width', 'longitude', 'status',
                  'buy', 'who', 'number', 'end_year')

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data['number']

        if len(number) < 4:
            raise ValidationError("Паролль слишком коротко")
        return cleaned_data

    def save(self, commit=True):
        home = super().save(commit=False)
        if commit:
            home.save()
        return home


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = NewUser
        fields = ('status', 'email', 'username', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']

        if len(password) < 6:
            raise ValidationError("Паролль слишком короткий min 6 ")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)


SubjectMetaInlineFormset = inlineformset_factory(
    Home,
    Photo,
    PhotoForm,
    extra=3,
    can_delete=False,
)


class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = ReportImage
        fields = ('image',)


ReportMetaInline = inlineformset_factory(
    Report,
    ReportImage,
    ReportPhotoForm,
    extra=5,
    can_delete=False,
)
