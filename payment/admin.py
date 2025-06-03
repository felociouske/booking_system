from django.contrib import admin, messages
from .models import Payment, PaymentInfo

@admin.action(description='Mark selected payments as approved')
def approve_payments(self, request, queryset):
    updated = queryset.update(status='approved')
    self.message_user(request, f"{updated} payment(s) marked as approved.", messages.SUCCESS)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_code', 'amount', 'status', 'date_submitted')
    list_filter = ('status', 'date_submitted')
    search_fields = ('transaction_code', 'user__username')
    actions = [approve_payments]

@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'recipient_name')
