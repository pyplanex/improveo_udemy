from django.contrib import admin
from .models import GeneralPost, ProblemPost, Comment
from .forms import PostForm
# Register your models here.


# class GeneralPostAdmin2(admin.ModelAdmin):
#     form = PostForm

class GeneralPostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'num_likes', 'author', 'created']
    exclude = ('liked',)

    class Meta:
        model = GeneralPost


class ProblemPostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'num_likes', 'author', 'created']
    fields = ('author', 'report', 'problem_reported', 'liked',)
    list_display_links = ('__str__', 'author',)
    list_filter = ('created',)

    search_fields = ('author__user__username',)

    class Meta:
        model = ProblemPost


admin.site.register(GeneralPost, GeneralPostAdmin)
admin.site.register(ProblemPost, ProblemPostAdmin)
admin.site.register(Comment)
