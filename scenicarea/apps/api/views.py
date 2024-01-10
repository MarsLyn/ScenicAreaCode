from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from .forms import ConcernForm, GiftRelationshipForm
from .models import Concern, Nexus, GiftStatus, Gift, GiftRelationship

from apps.merchant.forms import SingupForm
from apps.merchant.models import Commodity

from apps.conversation.models import Conversation, ConversationMessage

from apps.wallet.models import Wallet

# Create your views here.
def index(request):
    queryset_commodity = Commodity.objects.all()
    context = {
        'queryset': queryset_commodity
    }
    return render(request, 'api/index.html', context)

def details(request, id):
    obj_commodity = get_object_or_404(Commodity, id=id)
    context = {
        'obj': obj_commodity
    }
    return render(request, 'api/details.html', context)

def sing_up(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('api:log_in'))
    else:
        form = SingupForm()
    context = {
        'form': form
    }
    return render(request, 'api/sing_up.html', context)

def center(request):
    return render(request, 'api/center.html')

@login_required(login_url='/login/')
def conversation(request):
    conversations = Conversation.objects.select_related('commodity').filter(members__id__in=[request.user.id])
    context = {
        'conversations': conversations
    }
    return render(request, 'api/conversation.html', context)

@login_required(login_url='/login/')
def friend_list(request):
    concern = Concern.objects.filter(created_by=request.user, nexus__id=1)
    context = {
        'concern': concern,
    }
    return render(request, 'api/friend_list.html', context)

@login_required(login_url='/login/')
def search_friend(request):
    user = None
    query = request.GET.get('query')

    if query:
        user = User.objects.filter(username__icontains=query)

    if request.method == 'POST':
        concern = Concern.objects.filter(created_by=request.user, passive_by=request.POST.get('passive_by')).exists()
        if concern:
            return redirect(f'/friend/search/?query={query}')
        form = ConcernForm(request.POST)
        if form.is_valid():
            concern = form.save(commit=False)
            concern.nexus = Nexus.objects.get(id=1)
            concern.created_by = request.user
            concern.save()
            return redirect(f'/friend/search/?query={query}')
    else:
        form = ConcernForm()
    context = {
        'user': user,
        'query': query,
        'form': form,
    }
    return render(request, 'api/friend_search.html', context)

@login_required(login_url='/login/')
def delete_friend(request, id):
    Concern.objects.filter(id=id, created_by=request.user).delete()
    return redirect(reverse('api:friend_list'))

@login_required(login_url='/login/')
def gift_index(request):
    giftrelation = GiftRelationship.objects.filter(gift_user=request.user)
    context = {
        'giftrelation': giftrelation,
    }
    return render(request, 'api/gift.html', context)

@login_required(login_url='/login/')
def gift_receive_index(request):
    giftrelation = GiftRelationship.objects.filter(receive_user=request.user)
    context = {
        'giftrelation': giftrelation,
    }
    return render(request, 'api/gift.html', context)

@login_required(login_url='/login/')
def gift_details(request, id):
    giftrelation = GiftRelationship.objects.filter(Q(gift__id=id), Q(gift_user=request.user) | Q(receive_user=request.user)).last()
    context = {
        'giftrelation': giftrelation,
    }
    return render(request, 'api/gift_details.html', context)

@login_required(login_url='/login/')
def gift_receive(request, id):
    giftrelation = GiftRelationship.objects.filter(
        Q(gift__id=id),     
        Q(receive_user=request.user), 
        Q(status__id=1) | Q(status__id=3)
    ).first()
    giftrelation.status_id = 2
    giftrelation.save()
    return redirect(reverse('api:gift_details', kwargs={'id': id}))

@login_required(login_url='/login/')
def new_gift(request, id):
    concerns = None
    obj = get_object_or_404(Commodity, id=id)
    concerns = Concern.objects.filter(created_by=request.user)
    wallet = get_object_or_404(Wallet, user=request.user)
    if request.method == "POST":
        form = GiftRelationshipForm(request.POST)
        if wallet.balance > obj.price:
            if form.is_valid():
                gift = Gift.objects.create(commodity=obj)
                giftrelation = form.save(commit=False)
                giftrelation.gift = gift
                giftrelation.gift_user = request.user
                giftrelation.save()
                wallet.balance = F('balance') - obj.price
                wallet.save()
                return redirect(reverse('api:gift_index'))
        else:
            form.add_error(None, forms.ValidationError(('您的余额不足'), code=400))
    else:
        form = GiftRelationshipForm()
    context = {
        'obj': obj,
        'concerns': concerns,
        'form': form,
        'url': reverse('api:new_gift', kwargs={'id': obj.id}),
        'status': 1,
    }
    return render(request, 'api/new_gift.html', context)

@login_required(login_url='/login/')
def forward_gift(request, gift_id, good_id):
    concerns = None
    gift = get_object_or_404(Gift, id=gift_id)
    obj = get_object_or_404(Commodity, id=good_id)
    concerns = Concern.objects.filter(created_by=request.user)
    if request.method == "POST":
        form = GiftRelationshipForm(request.POST)
        if form.is_valid():
            GiftRelationship.objects.filter(gift=gift).update(forward=True)
            giftrelation = form.save(commit=False)
            giftrelation.gift = gift
            giftrelation.gift_user = request.user
            giftrelation.save()
            return redirect(reverse('api:gift_index'))
    else:
        form = GiftRelationshipForm()
    context = {
        'obj': obj,
        'concerns': concerns,
        'form': form,
        'url': reverse('api:forward_gift', kwargs={'gift_id': gift.id, 'good_id': obj.id}),
        'status': 3,
    }
    return render(request, 'api/new_gift.html', context)