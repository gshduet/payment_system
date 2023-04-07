from rest_framework import serializers

from payments.models import ChargingPaymentRequest, PrepaymentRequest


class ChargingPaymentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        models = ChargingPaymentRequest
        fields = (
            'user', 'method', 'order_id', 'order_name', 'status', 'requested_at'
            'total_amount', 'spent_prepayment_amount', 'final_charge_amount'
        )

    def validate(self, data):
        total_amount = data['total_amount']
        pre_panyment = data['pre_panyment']

        if total_amount < pre_panyment:
            pre_panyment = total_amount
        ...


class PrepaymentRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        models = PrepaymentRequest
        fields = (
            'user', 'method', 'order_id', 'order_name', 'status', 'requested_at'
            'total_amount', 'final_charge_amount'
        )

    