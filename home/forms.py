from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Faculty, Unit, Department, Position, Item
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_name', 'unit_short_name', 'unit_type',]

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_short_name', 'unit_id']

        labels = {
            'unit_id': 'Unit',
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_name', 'position_short_name',]

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class ItemForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = Item
    #     fields = ['item_no', 'item_description', 'position_id']
    #     labels = {
    #         'item_no': 'Item number',
    #         'position_id': 'Position',
    #     }
    #     help_texts = {
    #         'item_no': mark_safe(_('<small style="color:teal">Official item number from national government.</small>')),
    #     }
    #     widgets = {
    #         'item_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item number.'}),
    #         'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description.'})
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(ItemForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Save'))


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['department_id', 'position_id', 'faculty_no', 'last_name', 'first_name', 'middle_name', 'ext_name',
                  'address', 'gender', 'education', 'date_hired', 'email_address', 'facebook', 'remarks',
                  'contact_no', 'picture', 'date_promoted', 'date_started', 'date_end', 'item_status', 'is_active', 'is_promoted',
                  'employment_status', 'employment_type', 'item_no',]
        labels = {
            'department_id': mark_safe(_('<strong>Department</strong>')),
            'is_active': 'Active?',
            'is_promoted': 'Promoted?',
            'position_id': 'Rank/Position',
        }
        help_texts = {
            'faculty_no': mark_safe(_('<small style="color:teal">Official employee number.</small>')),
            'item_no': mark_safe(_('<small style="color:teal">Employment item number.</small>')),
            'position_id': mark_safe(_('<small style="color:teal">Academic Rank/Position.</small>')),
        }
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'education': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'item_status': forms.Select(attrs={'class': 'form-control'}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'date_hired': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_promoted': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_started': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email (i.e. jcl@usm.edu.ph)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address.'}),
            'faculty_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter faculty no.'}),
            'item_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item no.'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name.'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name.'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter middle name.'}),
            'ext_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name extension.'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter remarks.'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter facebook name'})

        }

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
