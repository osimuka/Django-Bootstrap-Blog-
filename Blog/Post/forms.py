from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_summernote.widgets import SummernoteWidget
from .models import BlogPost, BlogComments
from django import forms


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('image', 'title', 'post',)
        exclude = ('author', 'date', 'update_date')
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. The Big Apple !!!'}),
            "post": SummernoteWidget(attrs={'class': 'form-control'}),
        }


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        fields = ('comment', )
        widgets = {
            "comment": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'leave a comment...'}),
        }

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        # check if comment is longer than 30 characters
        if len(comment) < 30:
            raise forms.ValidationError("Comment character length must be greater than 30")
        return comment