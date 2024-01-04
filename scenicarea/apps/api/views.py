from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import ConcernForm
from .models import Concern, Nexus

from apps.merchant.forms import SingupForm
from apps.merchant.models import Commodity

from apps.conversation.models import Conversation, ConversationMessage

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
    Concern.objects.get(id=id).delete()
    return redirect(reverse('api:friend_list'))