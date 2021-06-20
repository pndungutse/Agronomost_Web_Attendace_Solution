from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email', 
                  'password1', 
                  'password2',
                  )
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
    
        for fieldname in ['username', 'email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(CreateUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        
        return user
        


