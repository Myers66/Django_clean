from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class Trade(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыто'),
        ('closed', 'Закрыто'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class TradeImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='trade_images/')

    def __str__(self):
        return f"Image for {self.trade.title}"