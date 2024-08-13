from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from ads.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View

def home(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

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
        categories = Category.objects.all()
        ads = Ad.objects.filter(user=request.user)
        return render(request, 'my_ads.html', {'ads': ads, 'categories': categories})
    
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
    categories = Category.objects.all()
    liked_by_user = Like.objects.filter(ad=ad, user=request.user).exists() if request.user.is_authenticated else False
    receiver = ad.user
     
    return render(request, 'ad_detail.html', {
        'ad': ad,
        'ad_images': ad_images,
        'categories': categories,
        'liked_by_user': liked_by_user,
        'receiver': receiver, 
    })

@login_required
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

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        formset = AdImageFormSet(request.POST, request.FILES, queryset=ad.images.all())

        if form.is_valid() and formset.is_valid():
            ad = form.save()

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                elif form.cleaned_data.get('image'):
                    image = form.save(commit=False)
                    image.ad = ad
                    image.uploaded_by = request.user
                    image.save()

            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
        formset = AdImageFormSet(instance=ad)

    return render(request, 'ad_edit.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Ad deleted successfully.')
        return redirect('my_ads')
    return render(request, 'confirm_delete.html', {'ad': ad})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Ad deleted successfully.')
        return redirect('my_ads')  

    return render(request, 'ad_confirm_delete.html', {'ad': ad})

