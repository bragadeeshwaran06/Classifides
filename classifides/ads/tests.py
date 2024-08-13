from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Category, Ad, Like, AdImage
from ads.forms import AdForm, AdImageForm
from django.core.files.uploadedfile import SimpleUploadedFile

UserModel = get_user_model()

class AdViewsTestCase(TestCase):
    
    def setUp(self):
        # Create a test user and log in
        self.client = Client()
        self.user = UserModel.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create some test categories and ads
        self.category = Category.objects.create(name='Test Category')
        self.ad = Ad.objects.create(
            title='Test Ad',
            description='Test Description',
            category=self.category,
            user=self.user
        )
        self.ad_image = AdImage.objects.create(image='Lambo1.jpg', uploaded_by=self.user, ad=self.ad)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_category_ads_view(self):
        response = self.client.get(reverse('category_ads', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertContains(response, 'Test Ad')

    def test_my_ads_view(self):
        response = self.client.get(reverse('my_ads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_ads.html')
        self.assertContains(response, 'Test Ad')

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad_detail.html')
        self.assertContains(response, 'Test Ad')

    def test_like_ad_view(self):
        response = self.client.post(reverse('like_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, ad=self.ad).exists())

    def test_post_ad_view(self):
        test_image = SimpleUploadedFile(name='Lambo1.jpg', content=b'test_image_content', content_type='image/jpeg')

        data = {
            'title': 'New Ad',
            'description': 'New Description',
            'category': self.category.id,
            'images-TOTAL_FORMS': 1,
            'images-INITIAL_FORMS': 0,
            'images-0-image': test_image,
        }

        response = self.client.post(reverse('post_ad'), data, format='multipart')
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_edit_ad_view(self):
        new_image = SimpleUploadedFile(name='Lambo1.jpg', content=b'new_file_content', content_type='image/jpeg')

        data = {
            'title': 'Updated Ad',
            'description': 'Updated Description',
            'images-TOTAL_FORMS': 1,
            'images-INITIAL_FORMS': 1,
            'images-0-id': self.ad_image.id,
            'images-0-image': new_image,  
            'images-0-DELETE': 'on',  
        }

        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), data, format='multipart')

        self.assertEqual(response.status_code, 200)  
        self.ad.refresh_from_db()   

    def test_delete_ad_view(self):
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())
