from django.shortcuts import render,HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import F

from .models import Wallet
from .forms import WalletForm

# Create your views here.
@login_required
def index(request):
    wallet = Wallet.objects.filter(user=request.user).exists()
    if wallet:
        wallet = Wallet.objects.get(user=request.user)
    else:
        wallet = Wallet.objects.create(user=request.user)
    context = {
        'wallet': wallet,
    }
    return render(request, 'wallet/index.html', context)

@login_required
def recharge(request, id):
    print(request.POST)
    wallet = get_object_or_404(Wallet, user=request.user, user__id=id)
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            wallet.balance = F('balance') + form.cleaned_data.get('balance')
            wallet.save()
            return redirect(reverse('wallet:index'))
    else:
        form = WalletForm()
    context = {
        'wallet': wallet,
        'form': form,
    }
    return render(request, 'wallet/recharge.html', context)