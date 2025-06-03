from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transaction_code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_submitted = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.transaction_code} - {self.status}"


class PaymentInfo(models.Model):
    phone_number = models.CharField(max_length=20, default="0755913939")
    recipient_name = models.CharField(max_length=100, default="MARTIN MUNGAI")

    def __str__(self):
        return f"{self.phone_number} - {self.recipient_name}"

    class Meta:
        verbose_name = "Payment Information"
        verbose_name_plural = "Payment Information"
