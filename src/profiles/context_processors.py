from .models import Profile


def profile_pic(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            profile_obj = Profile.objects.get(user=user)
            pic = profile_obj.profile_picture
        except Profile.DoesNotExist:
            pic = None

        return {'picture': pic}
    return {}


def get_profile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            profile_obj = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile_obj = None
        return {"profile":profile_obj}
    return {}
