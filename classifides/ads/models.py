from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('job', 'Job'),
        ('gig', 'Gig'),
        ('rental', 'Rental'),
        ('for_sale', 'For Sale'),
        ('service', 'Service'),
        ('event', 'Event'),
        ('class', 'Class'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Ad(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tags = TaggableManager()
    location = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField()
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    show_contact_info = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AdImage(models.Model):
    image = models.ImageField(upload_to='ad_images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'Image for {self.ad.title}'

    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, related_name='messages',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.timestamp}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'ad')