from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ads.models import Message, Ad,Category
from django.utils import timezone

class ChatViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Braga', password='vaghar@123456')
        self.user2 = User.objects.create_user(username='testpress', password='deamond@123')
        self.client.login(username='testpress', password='deamond@123')
        self.category = Category.objects.create(name="Cars")

        self.ad = Ad.objects.create(
            title='Test Ad',
            category=self.category,  
            user=self.user2,
            location='Test Location',
            postal_code='12345',
            description='Test Description',
            price=100.00
        )
        
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            ad=self.ad,
            content='Hello, this is a test message.',
            timestamp=timezone.now()
        )

    def test_conversation_view(self):
        response = self.client.get(reverse('conversation', args=[self.ad.id, self.user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertIn('messages', response.context)
        self.assertIn('other_user', response.context)
        self.assertIn('ad', response.context)

    def test_inbox_view(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'inbox.html')
        self.assertIn('conversations', response.context)

    def test_post_message(self):
        response = self.client.post(reverse('conversation', args=[self.ad.id, self.user2.id]), {
            'message': 'New message from test user.'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Message.objects.filter(content='New message from test user.').exists())
