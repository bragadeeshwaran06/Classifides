from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, Category
from .forms import CustomUserCreationForm

class RegistrationTests(TestCase):
    def test_register_user_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'abc@gmail.com',
            'password1': 'Braga@123456',
            'password2': 'Braga@123456',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Braga@123456',
            'password2': 'differentpassword',
        })
        self.assertContains(response, 'The two password fields didn’t match.')
        self.assertEqual(response.status_code, 200)

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Braga@123456')
        self.category = Category.objects.create(name='Test Category')
        self.ad = Ad.objects.create(title='Test Ad', user=self.user, category=self.category)

    def test_user_profile_accessible(self):
        self.client.login(username='testuser', password='Braga@123456')
        response = self.client.get(reverse('user_profile'))
        self.assertContains(response, 'Test Ad')
        self.assertContains(response, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_login_required(self):
        response = self.client.get(reverse('user_profile'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("user_profile")}')

class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Braga@123456')

    def test_logout(self):
        self.client.login(username='testuser', password='Braga@123456')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)

class CustomUserCreationFormTests(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Braga@123456',
            'password2': 'Braga@123456',
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_email_already_in_use(self):
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='Braga@123456')
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password1': 'Braga@123456',
            'password2': 'Braga@123456',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Email is already in use'])

    def test_passwords_do_not_match(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Braga@123456',
            'password2': 'differentpassword',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_email_field_required(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'password1': 'Braga@123456',
            'password2': 'Braga@123456',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])
