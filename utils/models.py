from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성시각')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시각')

    class Meta:
        abstract = True


class RequestData(TimeStampModel):
    """
    토스페이먼츠 결제생성API, 결제승인API 요청 생성 시 사용된 데이터
    """
    PAYMENT_METHOD_CHOICES = (
        ('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'),
        ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'),
        ('게임문화상품권', '게임문화상품권'),
    )
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), ('DONE', 'DONE'),
    )

    order_id = models.CharField(
        verbose_name=_('주문번호'), primary_key=True, max_length=64
    )
    method = models.CharField(
        verbose_name=_('결제수단'), max_length=10, choices=PAYMENT_METHOD_CHOICES,
    )
    total_amount = models.CharField(verbose_name=_('총 결제금액'), max_length=100)
    final_charge_amount = models.CharField(
        verbose_name=_('최종 결제 금액'), max_length=100
    )
    status = models.CharField(
        verbose_name=_('결제생성 결과'), 
        max_length=15, 
        choices=STATUS_CHOICES,
        help_text='결제생성 객체의 상태표시.\
            결제생성 완료 시 IN_PROGRESS\
            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED\
            결제 승인 완료 시 DONE'
    )
    requested_at = models.DateTimeField(
        verbose_name=_('결제생성시각'), blank=True, null=True
    )

    class Meta:
        abstract = True


class ResponseData(TimeStampModel):
    """
    토스페이먼츠 결제생성API, 결제승인API 응답 후 받은 데이터
    """
    PAYMENT_METHOD_CHOICES = (
        ('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'),
        ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'),
        ('게임문화상품권', '게임문화상품권'),
    )
    STATUS_CHOICES = (
        ('READY', 'READY'), ('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), 
        ('WAITTING_FOR_DEPOSIT', 'WAITTING_FOR_DEPOSIT'), ('CANCELED', 'CANCELED'),
        ('PARTIAL_CANCELED', 'PARTIAL_CANCELED'), ('ABORTED', 'ABORTED'),
        ('DONE', 'DONE'),
    )

    order_id = models.CharField(verbose_name=_('주문번호'), primary_key=True, max_length=64)
    order_name = models.CharField(verbose_name=_('결제내역'), max_length=100)
    method = models.CharField(
        verbose_name=_('결제수단'), max_length=10, choices=PAYMENT_METHOD_CHOICES,
    )
    payment_key = models.CharField(verbose_name=_('결제 키 값'), max_length=200)
    m_id = models.CharField(verbose_name=_('상점아이디'), max_length=14)
    version = models.CharField(verbose_name=_('Payment 객체 응답 버전'), max_length=11)
    last_transaction_key = models.CharField(verbose_name=_('마지막 거래 키 값'), max_length=64)
    status = models.CharField(
        verbose_name=_('결제생성 결과'), 
        max_length=20, 
        choices=STATUS_CHOICES,
        help_text='결제생성 객체의 상태표시.\
            결제생성 완료 시 IN_PROGRESS\
            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED\
            결제 승인 완료 시 DONE'
    )
    culture_expense = models.BooleanField(verbose_name=_('문화비 지출 여부'), default=False)
    use_escrow = models.BooleanField(verbose_name=_('에스크로 사용 여부'), default=False)
    secret = models.CharField(
        verbose_name=_('웹훅 정상여부 검증 값'), max_length=50, blank=True, null=True
    )
    type = models.CharField(verbose_name=_('결제타입정보'), max_length=10)
    country = models.CharField(verbose_name=_('결제국가정보'), max_length=3)
    currency = models.CharField(verbose_name=_('통화 단위'), max_length=5, default='KRW')
    total_amount = models.PositiveIntegerField(verbose_name=_('총 결제금액'))
    balance_amount = models.PositiveIntegerField(verbose_name=_('취소가능잔고'))
    supplied_amount = models.PositiveIntegerField(verbose_name=_('공급가액'))
    vat = models.PositiveIntegerField(verbose_name=_('부가세'))
    tax_free_amount = models.PositiveIntegerField(
        verbose_name=_('결제금액 중 면세액'), default=0
    )
    tax_exemption_amount = models.PositiveIntegerField(
        verbose_name=_('결제금액 중 과세제외금액'), default=0
    )
    requested_at = models.DateTimeField(
        verbose_name=_('결제생성시각'), blank=True, null=True
    )
    approve_at = models.DateTimeField(
        verbose_name=_('결제승인시각'), blank=True, null=True
    )

    receipt = models.JSONField(verbose_name=_('영수증 정보'), blank=True, null=True, default=dict)
    cashReceipt = models.JSONField(verbose_name=_('현금 영수증 정보'), blank=True, null=True, default=dict)
    cancels = models.JSONField(verbose_name=_('결제 취소 이력'), blank=True, null=True, default=dict)
    card = models.JSONField(verbose_name=_('카드 결제 시 제공받는 카드 정보'), blank=True, null=True, default=dict)
    failure = models.JSONField(verbose_name=_('결제 실패 정보'), blank=True, null=True, default=dict)
    easyPay = models.JSONField(verbose_name=_('간편결제 정보'), blank=True, null=True, default=dict)
    virtualAccount = models.JSONField(verbose_name=_(
        '가상계좌 결제 시 제공받는 가상계좌 정보'), blank=True, null=True, default=dict
    )
    transfer = models.JSONField(verbose_name=_('계좌이체 결제 시 제공받는 이체 정보'), blank=True, null=True, default=dict)
    giftCertificate = models.JSONField(verbose_name=_('상품권 결제 시 제공받는 결제 정보'), blank=True, null=True, default=dict)
    mobilePhone = models.JSONField(verbose_name=_('휴대폰 결제 시 제공받는 결제 정보'), blank=True, null=True, default=dict)
    discount = models.JSONField(verbose_name=_('카드사 즉시 할인 프로모션 정보'), blank=True, null=True, default=dict)

    class Meta:
        abstract = True