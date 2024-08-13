# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ads.models import Message, Ad
from django.contrib.auth.models import User
from chat.forms import MessageForm

@login_required
def send_message(request, ad_id, receiver_id):
    ad = get_object_or_404(Ad, id=ad_id)
    receiver = get_object_or_404(User, id=receiver_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.ad = ad
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'receiver': receiver, 'ad': ad})

@login_required
def message_list(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'message_list.html', {'messages': messages})

@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'conversation.html', {'messages': messages, 'other_user': other_user})
