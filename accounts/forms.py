from django import forms

from pagedown.widgets import PagedownWidget

from .models import Profile, Worker, Vendor, Client

class ProfileForm(forms.ModelForm):
    """ called only for update """
    bio = forms.CharField(widget=PagedownWidget(), required=False)
    birth_date = forms.CharField(widget=forms.SelectDateWidget(years=range(1900, 2100)), required=False)
    class Meta:
        model = Profile
        fields = [
            "bio",
            # "location",
            "birth_date", # user.username \\ user.last_name \\ user.first_name \\ user.password
            'user',
            'bank_acc',
        ]


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            "profile",
            "address",
            "kind",
            "work_on_wh",
            "work_on_vehicle",
            "work_on_dpt",
            "salary",
            "fired",
        ]
        # {self.profile.user.username}\n Address: {self.address.full_address}\n Kind: {self.kind}\n Work on: {workon}\nGet salary:{self.salary}\n Status: {fired}"

        # fields = [
        #     "kind",
        # ]
        # KIND_CHOICES = (
        #         ('', 'Select the kind'),
        #         ('pharmacist', 'pharmacist'), #First one is the value of select option and second is the displayed value in option
        #         ('HR', 'HR'),
        #         ('accounting_manager', 'accounting_manager'), #  достаточно 1-го на все предприятие, ведь система сама все балансы показывает
        #         ('director', 'director'),
        #         # ('forecast_manager', 'forecast_manager'), #  -------- не нужен, ведь система сама делает
        #         ('cleaner', 'cleaner'), 
        #         ('loader', 'loader'),
        #         ('driver', 'driver'), # 0.1
        #         # ('storekeeper_manager', 'storekeeper_manager'), #  -------- не нужен, так как нет склада своего
        #         # ('storekeeper', 'storekeeper'), #  -------- не нужен, так как нет склада своего, а за размещение в аптеке отвечают pharmacist и loader
        #         ('sys_admin', 'sys_admin'), #  2 на систему (посменно)
        #         # ('supply_chain_manager', 'supply_chain_manager'), #  -------- не нужен, ведь система сама делает
        #         )
        # widgets = {
        #     'kind': forms.Select(choices=KIND_CHOICES, attrs={'class': 'form-control'}),
        # }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            "organisation",
            "profile",
            "address",
        ]
        # fields = [
        #     "organisation",
        # ]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "profile"
        ]

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    # def clean_email(self):
    # #     email = self.cleaned_data.get('email')
    # #     email2 = self.cleaned_data.get('email2')
    # #     if email != email2:
    # #         raise forms.ValidationError("Emails must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")
    #     return email
