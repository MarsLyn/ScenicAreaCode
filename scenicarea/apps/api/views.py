from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required

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