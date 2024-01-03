from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Conversation
from .forms import ConversationMessageForm

from apps.merchant.models import Commodity

# Create your views here.
@login_required(login_url='/login/')
def new_conversation(request, id):
    # 获取要对话的商品
    obj_commodity = get_object_or_404(Commodity, id=id)
   
    if obj_commodity.user == request.user:
        # 如果创建对话的用户是这个商品的创建者
        # 自动定向到这个创建者的商品列表
        return redirect(reverse('merchant:index'))
    
    # 查找对话表中是否存在和这个商品相关的对话
    # 在过滤相关对话记录中关于创建对话用户的所有对话
    obj_conversation = Conversation.objects.filter(commodity=obj_commodity).filter(members__in=[request.user.id]).first()

    if obj_conversation:
        qs_message = obj_conversation.messages.all()
    else:
        qs_message = []

    if request.method == 'POST':
        # 把发送的信息放到form中验证
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            # 如果验证通过
            # 创建一条关于这个商品的对话
            # 保存创建对话的用户id和关于这个商品的创建者id
            if not obj_conversation:
                obj_conversation = Conversation.objects.create(commodity=obj_commodity)
                obj_conversation.members.add(request.user)
                obj_conversation.members.add(obj_commodity.user)
                obj_conversation.save()

            # 把发送的信息保存到信息表
            # 在将这条对话的id和创建对话的用户id保存到信息表
            form_conversation_message = form.save(commit=False)
            form_conversation_message.conversation = obj_conversation
            form_conversation_message.created_by = request.user
            form_conversation_message.save()

            # 保存完成重定向到对话页面
            return redirect(reverse('conversation:new', kwargs={'id': id}))
        
    else:
        form = ConversationMessageForm()
    
    context = {
        'form': form,
        'id': id,
        'queryset': qs_message,
    }
    return render(request, 'conversation/new.html', context)