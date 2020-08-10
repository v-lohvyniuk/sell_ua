from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from sell_auth.forms import RegistrationForm
from website.models import WebsiteUser


def registerPage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'sell_auth/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = WebsiteUser.objects.get(email=email)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.GET['next']
            return redirect(redirect_to)

    return render(request, 'sell_auth/login.html', {})
