# Generated by Django 4.1.7 on 2023-04-07 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrepaymentResponse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='주문번호')),
                ('order_name', models.CharField(max_length=100, verbose_name='결제내역')),
                ('method', models.CharField(choices=[('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'), ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'), ('게임문화상품권', '게임문화상품권')], max_length=10, verbose_name='결제수단')),
                ('payment_key', models.CharField(max_length=200, verbose_name='결제 키 값')),
                ('m_id', models.CharField(max_length=14, verbose_name='상점아이디')),
                ('version', models.CharField(max_length=11, verbose_name='Payment 객체 응답 버전')),
                ('last_transaction_key', models.CharField(max_length=64, verbose_name='마지막 거래 키 값')),
                ('status', models.CharField(choices=[('READY', 'READY'), ('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), ('WAITTING_FOR_DEPOSIT', 'WAITTING_FOR_DEPOSIT'), ('CANCELED', 'CANCELED'), ('PARTIAL_CANCELED', 'PARTIAL_CANCELED'), ('ABORTED', 'ABORTED'), ('DONE', 'DONE')], help_text='결제생성 객체의 상태표시.            결제생성 완료 시 IN_PROGRESS            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED            결제 승인 완료 시 DONE', max_length=20, verbose_name='결제생성 결과')),
                ('culture_expense', models.BooleanField(default=False, verbose_name='문화비 지출 여부')),
                ('use_escrow', models.BooleanField(default=False, verbose_name='에스크로 사용 여부')),
                ('secret', models.CharField(blank=True, max_length=50, null=True, verbose_name='웹훅 정상여부 검증 값')),
                ('type', models.CharField(max_length=10, verbose_name='결제타입정보')),
                ('country', models.CharField(max_length=3, verbose_name='결제국가정보')),
                ('currency', models.CharField(default='KRW', max_length=5, verbose_name='통화 단위')),
                ('total_amount', models.PositiveIntegerField(verbose_name='총 결제금액')),
                ('balance_amount', models.PositiveIntegerField(verbose_name='취소가능잔고')),
                ('supplied_amount', models.PositiveIntegerField(verbose_name='공급가액')),
                ('vat', models.PositiveIntegerField(verbose_name='부가세')),
                ('tax_free_amount', models.PositiveIntegerField(default=0, verbose_name='결제금액 중 면세액')),
                ('tax_exemption_amount', models.PositiveIntegerField(default=0, verbose_name='결제금액 중 과세제외금액')),
                ('requested_at', models.DateTimeField(blank=True, null=True, verbose_name='결제생성시각')),
                ('approve_at', models.DateTimeField(blank=True, null=True, verbose_name='결제승인시각')),
                ('receipt', models.JSONField(blank=True, default=dict, null=True, verbose_name='영수증 정보')),
                ('cashReceipt', models.JSONField(blank=True, default=dict, null=True, verbose_name='현금 영수증 정보')),
                ('cancels', models.JSONField(blank=True, default=dict, null=True, verbose_name='결제 취소 이력')),
                ('card', models.JSONField(blank=True, default=dict, null=True, verbose_name='카드 결제 시 제공받는 카드 정보')),
                ('failure', models.JSONField(blank=True, default=dict, null=True, verbose_name='결제 실패 정보')),
                ('easyPay', models.JSONField(blank=True, default=dict, null=True, verbose_name='간편결제 정보')),
                ('virtualAccount', models.JSONField(blank=True, default=dict, null=True, verbose_name='가상계좌 결제 시 제공받는 가상계좌 정보')),
                ('transfer', models.JSONField(blank=True, default=dict, null=True, verbose_name='계좌이체 결제 시 제공받는 이체 정보')),
                ('giftCertificate', models.JSONField(blank=True, default=dict, null=True, verbose_name='상품권 결제 시 제공받는 결제 정보')),
                ('mobilePhone', models.JSONField(blank=True, default=dict, null=True, verbose_name='휴대폰 결제 시 제공받는 결제 정보')),
                ('discount', models.JSONField(blank=True, default=dict, null=True, verbose_name='카드사 즉시 할인 프로모션 정보')),
                ('foreignEasyPay', models.JSONField(blank=True, default=dict, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prepayment_response', to=settings.AUTH_USER_MODEL, verbose_name='결제유저')),
            ],
            options={
                'db_table': 'prepayment_responses',
            },
        ),
        migrations.CreateModel(
            name='PrepaymentRequest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='주문번호')),
                ('method', models.CharField(choices=[('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'), ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'), ('게임문화상품권', '게임문화상품권')], max_length=10, verbose_name='결제수단')),
                ('total_amount', models.CharField(max_length=100, verbose_name='총 결제금액')),
                ('final_charge_amount', models.CharField(max_length=100, verbose_name='최종 결제 금액')),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), ('DONE', 'DONE')], help_text='결제생성 객체의 상태표시.            결제생성 완료 시 IN_PROGRESS            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED            결제 승인 완료 시 DONE', max_length=15, verbose_name='결제생성 결과')),
                ('requested_at', models.DateTimeField(blank=True, null=True, verbose_name='결제생성시각')),
                ('approve_at', models.DateTimeField(blank=True, null=True, verbose_name='결제승인시각')),
                ('order_name', models.CharField(default='선불금충전 대금 결제', max_length=100, verbose_name='결제내역')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prepayment_request', to=settings.AUTH_USER_MODEL, verbose_name='결제유저')),
            ],
            options={
                'db_table': 'prepayment_requests',
            },
        ),
        migrations.CreateModel(
            name='Prepayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='현재 선불금')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prepayment', to=settings.AUTH_USER_MODEL, verbose_name='소지유저')),
            ],
            options={
                'db_table': 'prepayments',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('amount', models.PositiveIntegerField(verbose_name='무료충전 금액')),
                ('number', models.CharField(max_length=20, unique=True, verbose_name='쿠폰번호')),
                ('is_used', models.BooleanField(default=False, verbose_name='사용여부')),
                ('deadline_at', models.DateTimeField(blank=True, null=True, verbose_name='사용기한')),
                ('used_at', models.DateTimeField(blank=True, null=True, verbose_name='사용된 시각')),
                ('is_delete', models.BooleanField(default=False, verbose_name='쿠폰소각 여부')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coupon', to=settings.AUTH_USER_MODEL, verbose_name='사용한 유저')),
            ],
            options={
                'db_table': 'coupons',
            },
        ),
        migrations.CreateModel(
            name='ChargingPaymentResponse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='주문번호')),
                ('order_name', models.CharField(max_length=100, verbose_name='결제내역')),
                ('method', models.CharField(choices=[('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'), ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'), ('게임문화상품권', '게임문화상품권')], max_length=10, verbose_name='결제수단')),
                ('payment_key', models.CharField(max_length=200, verbose_name='결제 키 값')),
                ('m_id', models.CharField(max_length=14, verbose_name='상점아이디')),
                ('version', models.CharField(max_length=11, verbose_name='Payment 객체 응답 버전')),
                ('last_transaction_key', models.CharField(max_length=64, verbose_name='마지막 거래 키 값')),
                ('status', models.CharField(choices=[('READY', 'READY'), ('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), ('WAITTING_FOR_DEPOSIT', 'WAITTING_FOR_DEPOSIT'), ('CANCELED', 'CANCELED'), ('PARTIAL_CANCELED', 'PARTIAL_CANCELED'), ('ABORTED', 'ABORTED'), ('DONE', 'DONE')], help_text='결제생성 객체의 상태표시.            결제생성 완료 시 IN_PROGRESS            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED            결제 승인 완료 시 DONE', max_length=20, verbose_name='결제생성 결과')),
                ('culture_expense', models.BooleanField(default=False, verbose_name='문화비 지출 여부')),
                ('use_escrow', models.BooleanField(default=False, verbose_name='에스크로 사용 여부')),
                ('secret', models.CharField(blank=True, max_length=50, null=True, verbose_name='웹훅 정상여부 검증 값')),
                ('type', models.CharField(max_length=10, verbose_name='결제타입정보')),
                ('country', models.CharField(max_length=3, verbose_name='결제국가정보')),
                ('currency', models.CharField(default='KRW', max_length=5, verbose_name='통화 단위')),
                ('total_amount', models.PositiveIntegerField(verbose_name='총 결제금액')),
                ('balance_amount', models.PositiveIntegerField(verbose_name='취소가능잔고')),
                ('supplied_amount', models.PositiveIntegerField(verbose_name='공급가액')),
                ('vat', models.PositiveIntegerField(verbose_name='부가세')),
                ('tax_free_amount', models.PositiveIntegerField(default=0, verbose_name='결제금액 중 면세액')),
                ('tax_exemption_amount', models.PositiveIntegerField(default=0, verbose_name='결제금액 중 과세제외금액')),
                ('requested_at', models.DateTimeField(blank=True, null=True, verbose_name='결제생성시각')),
                ('approve_at', models.DateTimeField(blank=True, null=True, verbose_name='결제승인시각')),
                ('receipt', models.JSONField(blank=True, default=dict, null=True, verbose_name='영수증 정보')),
                ('cashReceipt', models.JSONField(blank=True, default=dict, null=True, verbose_name='현금 영수증 정보')),
                ('cancels', models.JSONField(blank=True, default=dict, null=True, verbose_name='결제 취소 이력')),
                ('card', models.JSONField(blank=True, default=dict, null=True, verbose_name='카드 결제 시 제공받는 카드 정보')),
                ('failure', models.JSONField(blank=True, default=dict, null=True, verbose_name='결제 실패 정보')),
                ('easyPay', models.JSONField(blank=True, default=dict, null=True, verbose_name='간편결제 정보')),
                ('virtualAccount', models.JSONField(blank=True, default=dict, null=True, verbose_name='가상계좌 결제 시 제공받는 가상계좌 정보')),
                ('transfer', models.JSONField(blank=True, default=dict, null=True, verbose_name='계좌이체 결제 시 제공받는 이체 정보')),
                ('giftCertificate', models.JSONField(blank=True, default=dict, null=True, verbose_name='상품권 결제 시 제공받는 결제 정보')),
                ('mobilePhone', models.JSONField(blank=True, default=dict, null=True, verbose_name='휴대폰 결제 시 제공받는 결제 정보')),
                ('discount', models.JSONField(blank=True, default=dict, null=True, verbose_name='카드사 즉시 할인 프로모션 정보')),
                ('is_partial_cancelable', models.BooleanField(default=True, help_text='이 값이 False면 전액 취소만 가능', verbose_name='부분취소 가능여부')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='charging_reponse', to=settings.AUTH_USER_MODEL, verbose_name='결제유저')),
            ],
            options={
                'db_table': 'charging_responses',
            },
        ),
        migrations.CreateModel(
            name='ChargingPaymentRequest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성시각')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시각')),
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='주문번호')),
                ('method', models.CharField(choices=[('카드', '카드'), ('가상계좌', '가상계좌'), ('간편결제', '간편결제'), ('휴대폰', '휴대폰'), ('계좌이체', '계좌이체'), ('문화상품권', '문화상품권'), ('도서문화상품권', '도서문화상품권'), ('게임문화상품권', '게임문화상품권')], max_length=10, verbose_name='결제수단')),
                ('total_amount', models.CharField(max_length=100, verbose_name='총 결제금액')),
                ('final_charge_amount', models.CharField(max_length=100, verbose_name='최종 결제 금액')),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'IN_PROGRESS'), ('EXPIRED', 'EXPIRED'), ('DONE', 'DONE')], help_text='결제생성 객체의 상태표시.            결제생성 완료 시 IN_PROGRESS            IN_PROGRESS 단계에서 결제 승인 API 미호출 후 30분 경과 시 EXPIRED            결제 승인 완료 시 DONE', max_length=15, verbose_name='결제생성 결과')),
                ('requested_at', models.DateTimeField(blank=True, null=True, verbose_name='결제생성시각')),
                ('approve_at', models.DateTimeField(blank=True, null=True, verbose_name='결제승인시각')),
                ('order_name', models.CharField(default='차량충전 대금 결제', max_length=100, verbose_name='결제내역')),
                ('spent_prepayment_amount', models.CharField(default='0', max_length=100, verbose_name='선불금 사용금액')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='charging_request', to=settings.AUTH_USER_MODEL, verbose_name='결제유저')),
            ],
            options={
                'db_table': 'charging_requests',
            },
        ),
    ]
