from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile
from .forms import ProfileModelForm
# Create your views here.


def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.bio = form.cleaned_data.get('bio')
            instance.website = form.cleaned_data.get('website')
            instance.profile_picture = form.cleaned_data.get('profile_picture')
            form.save()

    context = {
        'object': profile,
        'form': form
    }

    return render(request, 'profiles/profile.html', context)

# def test_view(request):
#     hw = "Hello World"
#     return HttpResponse(hw)


# def test_view_1(request):
#     gs = "go to sleep"
#     return HttpResponse(gs)


# def test_view_2(request):
#     if request.user.is_authenticated:
#         user = request.user
#         profile = Profile.objects.get(user=user)
#     else:
#         profile = 'no profile'

#     context = {
#         'user': profile
#     }

#     return render(request, 'profiles/test.html', context)
