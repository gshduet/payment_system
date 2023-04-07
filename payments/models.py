from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampModel, RequestData, ResponseData


class ChargingPaymentRequest(RequestData):
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, 
        related_name='charging_request', verbose_name=_('결제유저')
    )
    order_name = models.CharField(
        verbose_name=_('결제내역'), default='차량충전대금', max_length=100
    )
    spent_prepayment_amount = models.CharField(
        verbose_name=_('선불금 사용금액'), max_length=100, default='0'
    )

    class Meta:
        db_table = 'charging_requests'

    def __str__(self):
        return self.order_id    


class PrepaymentRequest(RequestData):
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, 
        related_name='prepayment_request', verbose_name=_('결제유저')
    )
    order_name = models.CharField(
        verbose_name=_('결제내역'), max_length=100, default='선불금충전대금'
    )
    
    class Meta:
        db_table = 'prepayment_requests'

    def __str__(self):
        return self.order_id


class ChargingPaymentResponse(ResponseData):
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, 
        related_name='charging_reponse', verbose_name=_('결제유저')
    )
    is_partial_cancelable = models.BooleanField(
        verbose_name=_('부분취소 가능여부'), default=True, 
        help_text='이 값이 False면 전액 취소만 가능'
    )

    class Meta:
        db_table = 'charging_responses'

    def __str__(self):
        return self.order_id


class PrepaymentResponse(ResponseData):
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, 
        related_name='prepayment_response', verbose_name=_('결제유저')
    )
    foreignEasyPay = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        db_table = 'prepayment_responses'

    def __str__(self):
        return self.order_id


class Prepayment(TimeStampModel):
    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE, 
        related_name='prepayment', verbose_name=_('소지유저')
    )
    amount = models.PositiveIntegerField(verbose_name=_('현재 선불금'), default=0)

    class Meta:
        db_table = 'prepayments'

    def __str__(self):
        return self.user.email


class Coupon(TimeStampModel):
    user = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, 
        related_name='coupon', verbose_name=_('사용한 유저'), blank=True, null=True
    )
    amount = models.PositiveIntegerField(verbose_name=_('무료충전 금액'))
    number = models.CharField(verbose_name=_('쿠폰번호'), unique=True, max_length=20)
    is_used = models.BooleanField(verbose_name=_('사용여부'), default=False)

    deadline_at = models.DateTimeField(verbose_name=_('사용기한'), blank=True, null=True)
    used_at = models.DateTimeField(verbose_name=_('사용된 시각'), blank=True, null=True)
    is_delete = models.BooleanField(verbose_name=_('쿠폰소각 여부'), default=False)

    class Meta:
        db_table = 'coupons'

    def __str__(self):
        return self.id