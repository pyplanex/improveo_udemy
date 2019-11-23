from django import forms
from profiles.models import Profile
from django.http import HttpResponseRedirect


class FormUserRequiredMixin(object):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            form.instance.author = profile
            return super(FormUserRequiredMixin, self).form_valid(form)
        else:
            form.add_error(None, "user must be logged in")
            return self.form_invalid(form)
