from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ads.models import Message, Ad
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                ad=ad,
                content=content
            )
        return redirect('conversation', ad_id=ad_id, user_id=user_id)
    
    return render(request, 'conversation.html', {'messages': messages, 'other_user': other_user, 'ad': ad})

@login_required
def inbox(request):
    users = User.objects.filter(
        models.Q(sent_messages__receiver=request.user) |
        models.Q(received_messages__sender=request.user)
    ).distinct()
    
    conversations = []
    for user in users:
        last_message = Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(receiver=user)) |
            (models.Q(sender=user) & models.Q(receiver=request.user))
        ).order_by('-timestamp').first()
        conversations.append((user, last_message))
    
    return render(request, 'inbox.html', {'conversations': conversations})


@require_POST
def edit_message(request,message_id):
    message_id = request.POST.get('message_id')
    new_content = request.POST.get('new_message_content')

    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.content = new_content
    message.save()
    
    return redirect('conversation', ad_id=message.ad.id, user_id=message.receiver.id)

@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    ad_id = message.ad.id
    message.delete()
    
    return redirect('conversation', ad_id=ad_id, user_id=message.receiver.id)
