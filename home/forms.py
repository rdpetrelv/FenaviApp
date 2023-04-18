from django.contrib.auth.forms import UserCreationForm, UserModel
from django import forms
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario', min_length=5, max_length=150)
    first_name = forms.CharField(label='Nombre', min_length=1, max_length=50)
    last_name = forms.CharField(label='Apellido', min_length=1, max_length=50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    #class Meta:
     #   model = User
      #  fields = ("username","first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, *kwargs)
        for fieldname in ['username', 'first_name', 'last_name' , 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})    
""" 
    def save(self):
        user = User.objects.create_user(self.username, self.cleaned_data[self.email], self.password1)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.email = self.cleaned_data["Email"]
        if commit:
            user.save()
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.email = self.cleaned_data["Email"]
        return user """


class AuthenticationDropdown(forms.Form):
    username = forms.ChoiceField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AuthenticationDropdown, self).__init__(*args, **kwargs)
        for us in User.objects.all():
            choice = []
            choice.append(us.get_username())
        self.username.choices = choice


        
        



