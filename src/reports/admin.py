from django.contrib import admin
from .models import Report, ProblemReported

# Register your models here.

admin.site.register(Report)
admin.site.register(ProblemReported)
