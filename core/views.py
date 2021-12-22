import math

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from core.forms import ReportForm, UserForm, LoginForm, HomeForm, SubjectMetaInlineFormset, ReportMetaInline
from core.models import *


class HomeList(ListView):
    queryset = Home.objects.all()
    template_name = "homes.html"
    context_object_name = "homes"

    def get_queryset(self):
        query = self.request.GET.get('s', None)
        if query is None:
            return Home.objects.all()

        return Home.objects.filter(
            Q(city__iexact=query) | Q(price__iexact=query) | Q(class_home__iexact=query) |
            Q(floor__iexact=query) | Q(status__iexact=query) | Q(title__iexact=query) |
            Q(description__iexact=query) | Q(region__iexact=query)  | Q(company__iexact=query)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = Video.objects.all()
        return context


class Detail(DetailView):
    template_name = 'detail.html'
    queryset = Home.objects.all()
    context_object_name = 'detail'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        self.object.home_count()
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = Video.objects.all()
        return context


def ipoteka(request):
    if request.method == 'POST':
        summa = request.POST['summa']
        payment = request.POST['payment']
        year = request.POST['year']
        percent = request.POST['percent']
        summa = int(summa)
        payment = int(payment)
        year = int(year)
        percent = float(percent)

        if summa > 0 and payment > 0 and year > 0 and percent > 0 and year < 15:
            how_payment = (summa / 100) * 30
            if payment >= how_payment:
                month_percent = percent / 12 / 100
                all_percent = math.pow(1 + month_percent, (year * 12))
                month_money = (summa - payment) * month_percent * all_percent / (all_percent - 1)
                percent_part = (summa - payment) * month_percent
                summ_part = month_money - percent_part
                real_month_money = round(percent_part + summ_part)
                over_payment = round(month_money * (year * 12) - (summa - payment))

                context = {'money': real_month_money,
                           'over': over_payment
                           }
                return render(request, 'ipoteka.html', context)
            else:
                messages.debug(request, 'Сумма начального взноса должно быть больше 30% ')
                return render(request, 'ipoteka.html', {})
        else:
            messages.warning(request, 'вы что то пропустили или не правильно заполнили')
            return render(request, 'ipoteka.html', {})
    else:
        return render(request, 'ipoteka.html', {})


def create_report(request, my_id):
    report_id = Home.objects.get(id=my_id)

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        form_photo = ReportMetaInline(request.POST, request.FILES, instance=form.instance)

        if form.is_valid():
            r = Report.objects.all()
            report_home = Report.call_home(r)
            report_id = report_home
            report_id.save()
            form.save()
            form_photo.save()
            messages.success(request, 'successfully')
            return render(request, 'report.html', {})
        else:
            messages.error(request, 'error')
            return render(request, 'report.html', {})

    form = ReportForm()
    form_photo = ReportMetaInline()
    return render(request, "report.html", {
        'form': form,
        'form_photo': form_photo,
    })


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if request.user.is_authenticated:
                messages.success(request, "successfully")

            else:
                messages.debug(request, 'authenticated пошло не так ')
    else:
        form = UserForm()

    context = {
        "form": form
    }
    return render(request, "register.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            messages.success(request, "successfully")
            if request.user.is_authenticated:
                login(request, user)
                messages.success(request, "successfully")
                return redirect("/homes/")
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, "login.html", context={
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect("/login/")


def add_home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = HomeForm(request.POST, request.FILES)
            form_photo = SubjectMetaInlineFormset(request.POST, request.FILES, instance=form.instance)

            if form.is_valid():
                form.save()
                form_photo.save()
                return redirect('/homes/')
            else:
                return form, form_photo

    form = HomeForm()
    form_photo = SubjectMetaInlineFormset()
    return render(request, "create.html", {
        'form': form,
        'form_photo': form_photo,
    })


class UserDetail(DetailView):
    template_name = 'user.html'
    queryset = NewUser.objects.all()
    context_object_name = 'user'


def test(request):
    v = Video.objects.get(id=1)
    return render(request, 'map.html', {"v": v})
