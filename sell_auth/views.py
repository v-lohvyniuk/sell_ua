from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from sell_auth.forms import RegistrationForm


def registerPage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'sell_auth/register.html', context)
