from .models import Profile
from django import forms


class ProfileModelForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'Few words about you...',
            'rows': 3,
        }
    ))

    website = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'your website'
        }
    ))

    class Meta:
        model = Profile
        fields = ('bio', 'website', 'profile_picture')
