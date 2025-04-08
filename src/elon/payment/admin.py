from django.contrib import admin
from .models import PaymentType, Orders, Transaction, Balance, Service


class OrdersAdmin(admin.ModelAdmin):
    fields = ('amount', 'status', 'service', 'user')
    list_display = ("id", "service", "amount", "status", "user", "created")
    list_display_links = ("id", )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "orders",  "payment_type", "price", "status", "transaction_id", "created")
    list_display_links = ('id', )


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction",  "debit", "credit", "user", "created")
    list_display_links = ('id', )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "alias",  "title")


admin.site.register(PaymentType)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Service, ServiceAdmin)
