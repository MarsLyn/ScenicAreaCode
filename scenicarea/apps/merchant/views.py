from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, OuterRef, Subquery


from .models import Commodity, AssistantImages
from .forms import GoodAddForm, AssistantImagesForm, AsInlineFormSet, SingupForm

from apps.conversation.models import Conversation, ConversationMessage
from apps.conversation.forms import ConversationMessageForm

# Create your views here.
@login_required
def index(request):
    queryset = Commodity.objects.filter(user=request.user)
    context = {
        'queryset': queryset,
        'paginator': queryset.count()
    }
    return render(request, 'merchant/index.html', context)

@login_required
def details(request, id):
    obj_good = get_object_or_404(Commodity, id=id, user=request.user)
    # obj_as_image = get_object_or_404(AssistantImages, id=id)

    good_form = GoodAddForm(request.POST or None, request.FILES or None, instance=obj_good)
    # as_image_form = AssistantImagesForm(request.POST or None, request.FILES or None, instance=obj_as_image)

    if request.method == 'POST':
        if good_form.is_valid():
            good_form.save()
            return redirect(reverse('merchant:index'))
        
    context = {
        'good_form': good_form,
        # 'as_image_form': as_image_form,
        'id': id
    }
    return render(request, 'merchant/details.html', context)

@login_required
def delete_good(request, id): 
    obj = get_object_or_404(Commodity, id=id, user=request.user)  
    if request.method == 'POST':
        obj.delete()
        return redirect(reverse('merchant:index'))
    context = {
        'obj': obj,
        'referer': request.headers['Referer']
    }
    return render(request, 'merchant/delete.html', context)

@login_required
def create_good(request): 
    if request.method == 'POST':
        good_form = GoodAddForm(request.POST, request.FILES)
        as_image_form = AssistantImagesForm(request.POST, request.FILES)
        if good_form.is_valid() and as_image_form.is_valid():
            obj_good = good_form.save(commit=False)
            obj_good.user = request.user
            obj_as_image = as_image_form.save(commit=False)
            obj_as_image.commodity = obj_good
            obj_good.save()
            obj_as_image.save()
            return redirect(reverse('merchant:index'))
    else:
        good_form = GoodAddForm()
        as_image_form = AssistantImagesForm()
    context = {
        'good_form': good_form,
        'as_image_form': as_image_form,
    }
    return render(request, 'merchant/create.html', context)

def sing_up(request):
    if request.method == "POST":
        print(request.POST)
        form = SingupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('merchant:log_in'))
    else:
        form = SingupForm()
    context = {
        'form': form
    }
    return render(request, 'merchant/sing_up.html', context)

@login_required
def search_good(request):
    query = request.GET.get('query')
    if query:
        queryset = Commodity.objects.filter(user=request.user, title__icontains=query)
    else:
        queryset = Commodity.objects.filter(user=request.user)
    context = {
        'query': query,
        'queryset': queryset,
        'paginator': queryset.count()
    }
    return render(request, 'merchant/index.html', context)

@login_required
def merchant_conversation(request):
    subquery1 = ConversationMessage.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-create_date').values('content')[:1]

    subquery2 = Conversation.objects.filter(
        commodity=OuterRef('commodity')
    ).values('commodity__title')[:1]

    conversations = Conversation.objects.annotate(
        latest_message_content=Subquery(subquery1),
        latest_message_sender=Subquery(subquery1.values('created_by__username')),
        latest_message_timestamp=Subquery(subquery1.values('create_date')),
        latest_commodity_title = Subquery(subquery2.values('commodity__title')),
        latest_commodity_picture = Subquery(subquery2.values('commodity__picture')),
    ).filter(members__id__in=[request.user.id])

    # print(conversations)
    # print(conversations.query)
    context = {
        'queryset': conversations,
        # 'paginator': qs_com.count()
    }
    return render(request, 'merchant/conversation.html', context)
    # return HttpResponse('ok')


@login_required
def merchant_message(request, id):
    qs_messages = ConversationMessage.objects.select_related('conversation', 'created_by').filter(
        conversation__id__in=[id]
    ).values(
        'created_by',
        'created_by__username',
        'content',
        'create_date',
    )
    obj = get_object_or_404(Conversation, id=id)
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            form_conversation_message = form.save(commit=False)
            form_conversation_message.conversation = obj
            form_conversation_message.created_by = request.user
            form_conversation_message.save()

            return redirect(reverse('merchant:message_send', kwargs={'id': id}))

    form = ConversationMessageForm()
    context = {
        'queryset': qs_messages,
        'form': form,
        'id': id,
    }
    return render(request, 'merchant/message_inbox.html', context)