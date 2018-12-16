from .models import Post
from django.core.exceptions import ValidationError
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'title', 'author', 'content', 'password' ]
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if self.instance.pk:  # on Update
            if password != self.instance.password:
                raise ValidationError("Wrong password.", code='wrong_password')

        return password
