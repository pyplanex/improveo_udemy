from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ProblemReported, Report
from profiles.models import Profile
from posts.models import ProblemPost


@receiver(post_save, sender=ProblemReported)
def post_save_report(sender, instance, created, *args, **kwargs):
    if created:
        try:
            id_ = instance.report.id
            rep = Report.objects.get(id=id_)
        except:
            rep = None

        if rep is not None:
            user = instance.user
            author = Profile.objects.get(user=user)
            ProblemPost.objects.create(
                author=author, report=rep, problem_reported=instance)
