from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ads.models import Message, Ad
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.http import require_POST
from chat.forms import MessageForm

@login_required
def conversation(request, ad_id, user_id):
    ad = get_object_or_404(Ad, id=ad_id)
    other_user = get_object_or_404(User, id=user_id)
        
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user),
        ad=ad
    ).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.ad = ad
            message.save()
            return redirect('conversation', ad_id=ad_id, user_id=user_id)
    else:
        form = MessageForm()
    
    return render(request, 'conversation.html', {'messages': messages, 'other_user': other_user, 'ad': ad,'form': form})

@login_required
def inbox(request):
    users = User.objects.filter(
        models.Q(sent_messages__receiver=request.user) |
        models.Q(received_messages__sender=request.user)
    ).distinct()
    
    conversations = []
    for user in users:
        last_message = Message.objects.filter(
            models.Q(sender=request.user, receiver=user) |
            models.Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        conversations.append((user, last_message))
    
    return render(request, 'inbox.html', {'conversations': conversations})

@require_POST
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    form = MessageForm(request.POST, instance=message)

    if form.is_valid():
        form.save() 
        return redirect('conversation', ad_id=message.ad.id, user_id=message.receiver.id)
    
    return render(request, 'conversation.html', {
        'messages': Message.objects.filter(
            models.Q(sender=request.user, receiver=message.receiver) |
            models.Q(sender=message.receiver, receiver=request.user),
            ad=message.ad
        ).order_by('timestamp'),
        'other_user': message.receiver,
        'ad': message.ad,
        'form': form
    })

@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    ad_id = message.ad.id
    message.delete()
    
    return redirect('conversation', ad_id=ad_id, user_id=message.receiver.id)
