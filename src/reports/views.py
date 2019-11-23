from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReportForm, ProblemReportedForm, ReportSelectLineForm, ReportResultForm
from .models import Report, ProblemReported
from areas.models import ProductionLine
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, FormView
from django.urls import reverse_lazy

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


@login_required
def get_generated_problems_in_pdf(request):

    # queryset
    problems = ProblemReported.objects.problems_from_today()

    # context passed in the template
    context = {'problems': problems}

    # render
    html_string = render_to_string(
        'reports/problems.html', context)
    # html = HTML(string=html_string)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=problem_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required
def main_report_summary(request):
    try:
        day = request.session.get('day', None)
        prod_id = request.session.get('production_line', None)
        production_line = ProductionLine.objects.get(id=prod_id)
        execution = Report.objects.get_by_line_and_day(
            day, prod_id).aggregate_execution()['execution__sum']
        plan = Report.objects.get_by_line_and_day(
            day, prod_id).aggregate_plan()['plan__sum']
        problems = ProblemReported.objects.get_problems_by_day_and_line(
            day, production_line)
    except:
        return redirect('reports:select-view')

    context = {
        'execution': execution,
        'plan': plan,
        'problems_reported': problems,
        'day': day,
        'line': production_line,
    }

    del request.session['day']
    del request.session['production_line']

    return render(request, 'reports/summary.html', context)


class SelectView(LoginRequiredMixin, FormView):
    template_name = 'reports/select.html'
    form_class = ReportResultForm
    success_url = reverse_lazy('reports:summary-view')

    def form_valid(self, form):
        self.request.session['day'] = self.request.POST.get('day', None)
        self.request.session['production_line'] = self.request.POST.get(
            'production_line', None)
        print(self.request.session['day'])
        return super(SelectView, self).form_valid(form)


class HomeView(FormView):
    template_name = 'reports/home.html'
    form_class = ReportSelectLineForm

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, *args, **kwargs):
        prod_line = self.request.POST.get("prod_line")
        return redirect('reports:report-view', production_line=prod_line)


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update.html'

    def get_success_url(self):
        return self.request.path


@login_required
def delete_view(request, *args, **kwargs):
    r_id = kwargs.get("pk")
    obj = Report.objects.get(id=r_id)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def report_view(request, production_line):
    form = ReportForm(request.POST or None, production_line=production_line)
    pform = ProblemReportedForm(request.POST or None)
    queryset = Report.objects.filter(production_line__name=production_line)
    line = get_object_or_404(ProductionLine, name=production_line)

    if 'submitbtn1' in request.POST:
        r_id = request.POST.get("report_id")
        print(r_id)

        if pform.is_valid():
            report = Report.objects.get(id=r_id)
            print("data here")
            obj = pform.save(commit=False)
            obj.user = request.user
            obj.report = report
            obj.save()
            # form = ReportForm()
            # pform = ProblemReportedForm()
            return redirect(request.META.get('HTTP_REFERER'))

    elif 'submitbtn2' in request.POST:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.production_line = line
            obj.save()
            # form = ReportForm()
            # pform = ProblemReportedForm()
            return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'pform': pform,
        'object_list': queryset,
    }

    return render(request, 'reports/report.html', context)
