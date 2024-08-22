from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from ads.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.http import Http404
from django.views.decorators.http import require_POST

def home(request):
    category_id = request.GET.get('category')
    ads = Ad.objects.filter(category_id=category_id) if category_id else Ad.objects.order_by('-created_at')[:10]
    categories = Category.objects.all()

    return render(request, 'base.html', {
        'ads': ads,
        'categories': categories,
        'selected_category': category_id,
    })

def category_ads(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.objects.filter(category=category).prefetch_related('images')
    categories = Category.objects.all()
    return render(request, 'category.html', {
        'category': category,
        'ads': ads,
        'categories': categories,
    })

class MyAdsView(View):
    @method_decorator(login_required)
    def get(self, request):
        ads = Ad.objects.filter(user=request.user)
        return render(request, 'my_ads.html', {'ads': ads,})
    
    @method_decorator(login_required)
    def post(self, request):
        ad_id = request.POST.get('ad_id')
        if ad_id:
            ad = get_object_or_404(Ad, id=ad_id)
            ad.delete()
            messages.success(request, 'Ad deleted successfully.')
        return redirect('my_ads')

@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad_images = ad.images.all()
    liked_by_user = Like.objects.filter(ad=ad, user=request.user).exists() if request.user.is_authenticated else False
    receiver = ad.user
     
    return render(request, 'ad_detail.html', {
        'ad': ad,
        'ad_images': ad_images,
        'liked_by_user': liked_by_user,
        'receiver': receiver, 
    })

@login_required
@require_POST
def like_ad(request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id)
        existing_like = Like.objects.filter(user=request.user, ad=ad).first()
        
        if existing_like:
            existing_like.delete()

        else:
            Like.objects.create(user=request.user, ad=ad)

        return redirect('ad_detail', ad_id=ad.id)

@login_required
def post_ad(request):
    if request.method == 'POST':
        ad_form = AdForm(request.POST, request.FILES)
        ad_image_form = AdImageForm()
        if ad_form.is_valid():
            ad = ad_form.save(commit=False)
            ad.user = request.user
            ad.save()

            
            images = request.FILES.getlist('images')
            for image in images:
                AdImage.objects.create(image=image, uploaded_by=request.user, ad=ad)

            return redirect('home')
    else:
        ad_form = AdForm()
        ad_image_form = AdImageForm()

    return render(request, 'post_ad.html', {'ad_form': ad_form, 'ad_image_form': ad_image_form})

from django.http import JsonResponse

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        raise Http404("You do not have permission to edit this ad.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)

        if form.is_valid():
            # Save the ad details first
            form.save()

            # Handle new image uploads
            if 'images' in request.FILES:
                for file in request.FILES.getlist('images'):
                    AdImage.objects.create(ad=ad, image=file, uploaded_by=request.user)

            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)

    images = AdImage.objects.filter(ad=ad)
    return render(request, 'ad_edit.html', {
        'form': form,
        'ad': ad,
        'images': images,
    })

@login_required
def delete_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        image = get_object_or_404(AdImage, id=image_id, ad__user=request.user)
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_POST
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    
    if ad.user != request.user:
        messages.error(request, 'You do not have permission to delete this ad.')
        return redirect('my_ads')

    ad.delete()
    messages.success(request, 'Ad deleted successfully.')
    return redirect('my_ads')