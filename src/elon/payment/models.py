from django.conf import settings
from django.db import models
from django.db.models import JSONField
from . import Status
from . import default_title, default_services

def lang_dict_field():
    return {'description_ru': '', 'description_uz': ''}


class Service(models.Model):
    title = models.JSONField(default=default_title)
    services = models.JSONField(default=default_services)
    description = JSONField(blank=False, null=False, default=lang_dict_field)
    is_active = models.BooleanField(default=True, null=False)
    sort_order = models.IntegerField(db_index=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    alias = models.CharField('alias', max_length=255, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"
        ordering = ["-created", ]


class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name="transaction_services", )
    amount = models.IntegerField(blank=False, null=False, )
    status = models.SmallIntegerField(default=0, )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="user_orders",
        on_delete=models.SET_NULL,
    )

    ad = models.ForeignKey(
        "ads.Ad", related_name="order_ad", blank=True, null=True, on_delete=models.SET_NULL,
    )

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created", ]

class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    title = JSONField(blank=False, null=False, default=lang_dict_field)
    is_active = models.BooleanField('is_active', default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment type"
        verbose_name_plural = "Payment types"
        ordering = ["-created", ]

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    orders = models.ForeignKey(Orders, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                 related_name="transaction_orders")
    payment_type = models.ForeignKey(PaymentType, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="payment_type",)
    price = models.IntegerField(blank=False, null=False, )
    status = models.SmallIntegerField(default=1, choices=Status.CHOICES, )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paydoc_id = models.BigIntegerField(blank=True, null=True)
    receipt_id = models.CharField(max_length=100, blank=True, null=True)
    pay_time = models.CharField(max_length=20, blank=True, null=True)
    pay_time_datetime = models.CharField(max_length=20, blank=True, null=True)
    perform_time = models.DateTimeField(blank=True, null=True)
    cancel_time = models.DateTimeField(blank=True, null=True)
    reason = models.SmallIntegerField(blank=True, null=True, )
    receivers = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.id, self.orders)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created", ]


class Balance(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, blank=False, null=False, on_delete=models.CASCADE,
                                 related_name="transaction_balance", )
    debit = models.IntegerField(blank=True, null=False, default=0,)
    credit = models.IntegerField(blank=True, null=False, default=0, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        related_name="balance_user"
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return '%s (%s)' % (self.transaction, self.created)

    class Meta:
        verbose_name = "backend_Balance"
        verbose_name_plural = "backend_Balance"
        ordering = ["-created", ]
