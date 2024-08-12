from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ads.models import Ad, Message

@login_required
def ad_chat(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user is None:

        return render(request, 'chat/ad_chat.html', {
            'ad': ad,
            'messages': [],
            'error': 'No valid user for this ad.',
        })

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            try:
                Message.objects.create(sender=request.user, receiver=ad.user, content=content, ad=ad)
            except Exception as e:
                # Log the error or handle it as needed
                return render(request, 'chat/ad_chat.html', {
                    'ad': ad,
                    'messages': Message.objects.filter(ad=ad).order_by('timestamp'),
                    'error': str(e),
                })

    messages = Message.objects.filter(ad=ad).order_by('timestamp')
    return render(request, 'chat/ad_chat.html', {
        'ad': ad,
        'messages': messages,
    })
