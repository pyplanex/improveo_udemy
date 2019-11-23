import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
from categories.models import Category
from areas.models import ProductionLine
from django.urls import reverse
from django.db.models import Sum, Avg
import random
from datetime import datetime
# Create your models here.

# hours= (
#     ("1", "1"),
#     ("2", "2"),
#     ("3", "3"),
#     ...
# )

hours = ([(str(x), str(x)) for x in range(1, 25)])

el = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
      'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

'''
get_queryset() - method responsible for retrieving all the data from the database according to
               the defined querysets
super()        -  method which returns a proxy object that allows you to refer parent class

def get_all_active(self):
    return super().get_queryset().filter(draft=False)
    return Post.objects.filter(draft=False)
'''


class ReportQueryset(models.QuerySet):
    def get_by_line_and_day(self, day, line_id):
        return self.filter(day=day, production_line__id=line_id)

    def aggregate_execution(self):
        return self.aggregate(Sum('execution'))

    def aggregate_plan(self):
        return self.aggregate(Sum('plan'))


class ReportManager(models.Manager):
    def get_queryset(self):
        return ReportQueryset(self.model, using=self._db)

    def get_by_line_and_day(self, day, line_id):
        return self.get_queryset().get_by_line_and_day(day, line_id)

    def aggregate_execution(self):
        return self.get_queryset().aggregate_execution()

    def aggregate_plan(self):
        return self.get_queryset().aggregate_plan()


class Report(models.Model):
    day = models.DateField(default=timezone.now)
    start_hour = models.CharField(max_length=2, choices=hours)
    end_hour = models.CharField(max_length=2, choices=hours)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    plan = models.PositiveIntegerField()
    execution = models.PositiveIntegerField()
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()

    def get_day(self):
        return self.day.strftime('%Y/%m/%d')

    def get_absolute_url(self):
        return reverse("reports:update-view", kwargs={'production_line': self.production_line, 'pk': self.pk, })

    def __str__(self):
        return "{}-{}-{}".format(self.start_hour, self.end_hour, self.production_line)

    class Meta:
        ordering = ('-created',)


def random_code():
    random.shuffle(el)
    code = [str(x) for x in el[:12]]
    str_code = ''.join(code)

    return str_code


class ProblemReportedManager(models.Manager):

    def get_problems_by_day_and_line(self, day, line):
        return super().get_queryset().filter(report__day=day, report__production_line__name=line)

    def problems_from_today(self):
        now = datetime.now().strftime('%Y-%m-%d')
        return super().get_queryset().filter(report__day=now)


class ProblemReported(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(
        max_length=12, unique=True, blank=True, default=random_code)
    breakdown = models.PositiveIntegerField()
    public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProblemReportedManager()

    def __str__(self):
        return "{}-{}".format(self.category.name, self.description[:20])

    class Meta:
        verbose_name = "Problem Reported"
        verbose_name_plural = "Problems Reported"
