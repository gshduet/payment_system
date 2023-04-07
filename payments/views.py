import base64, json, os, requests
from datetime import datetime
import random

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from payments.models import ChargingPaymentRequest, PrepaymentRequest
from payments.serializers import ChargingPaymentRequestSerializer, PrepaymentRequestSerializer


def index(request):
    return render(request, 'payments/index.html')

def window(request):
    return render(request, 'payments/window.html')

class PaymentRequestView(APIView):
    """
    PG사(토스페이먼츠)와 연동하여 결제를 진행하는 상황(가정)이므로 토스페이먼츠에게 보낼 요청을 만들어야합니다.
    사용자가 서비스를 사용 중 결제를 해야하는 상황은 2가지(전기차 충전 대금 결제, 선불금 충전 대금 결제)입니다.
    각각 다른 url에서 요청이 들어오나 결제는 하나의 인터페이스를 통과할 예정입니다.
    예시는 전기차 충전 대금 결제 상황을 우선으로 작성되었습니다. 

    1.  전기차 충전 완료 후 클라이언트로부터 세 가지 정보가 들어옵니다.
        {
            'method': 'str',
            'totalAmount': 'int',
            'advancePanyment': 'int'
        }
            a. 각각 결제수단, 총 결제금액, 현재 결제 중 사용하고자 하는 선불금을 뜻합니다.
            b. 현재 사용 가능한 결제수단은 카드 뿐입니다.
            c. 사용하고자 하는 선불금이 현재 충전되어 있는 선불금보다 적을 경우 에러를 발생하고 적절한 상태코드와 메시지를 반환합니다.
    
    2.  해당 정보들을 바탕으로 결제 생성 요청을 제작합니다.
        결제 생성 요청에 필요한 파라미터는 다음과 같습니다.
        {
            'method': 'str',
            'amount': 'str',
            'orderId': 'str',
            'orderName': 'str'
            'successUrl': 'str',
            'failUrl': 'str'
        }
        각각 결제수단, 결제금액(총 결제금액 - 선불금), 주문ID, 주문명, 
        결제 성공시 리다이렉트 될 URL, 결제 실패시 리다이렉트 될 URL을 뜻합니다.

            a.  orderID의 경우 영문 대소문자, 숫자, 특수문자('-', '_')를 사용하여 임의로 구성하여야 합니다.
            b.  orderName의 경우 주문하고자 하는 상품 이름으로 현재 서비스에선 
                선불금 충전 or 충전대금 결제 상황이 존재므로 상황에 맞는 이름이 들어갑니다.

    3.  위의 파라미터를 가진 Request Body를 토스페이먼츠 url(POST https://api.tosspayments.com/v1/payments)로 
        전송하여 응답을 받아옵니다.

    4.  결제 생성 응답 결과는 총 5가지이며 
        응답 성공시 200 상태코드와 Payment 객체를, 응답 실패 시 400 상태코드와 에러 객체를 받습니다.

    5. 위의 과정에서 생산한 요청은 DB에 저장됩니다.
    """

    def make_order_id(requested_at):
        """
        결제ID는 토스페이먼츠 규정상 영문 대소문자, 숫자, 특수문자('-', '_')를 사용하여 임의로 구성하여야 하며
        현재는 결제생성 요청 생성시각+6자리 임의의 정수로 구성됨
        """
        current_time = requested_at.strftime('%Y%m%d%H%M%S')
        random_number = random.randrange(100000,999999)
        ret = str(current_time) + str(random_number)

        return ret

    def post(self, request):
        method = request.GET.get('method')
        order_name = request.GET.get('order_name')
        total_amount = int(request.GET.get('totalAmount'))
        spent_prepayment_amount = int(request.GET.get('advancePanyment', '0'))

        requested_at = datetime.now()

        final_charge_amount = str(total_amount - spent_prepayment_amount)
        order_id = self.make_order_id(requested_at)
        success_url = 'http://localhost:8000/success'
        fail_url = 'http://localhost:8000/fail'

        url = 'https://api.tosspayments.com/v1/payments'
        secret_key = os.environ.get('toss_secret_key')
        userpass = secret_key + ':'
        encoded_u = base64.b64encode(userpass.encode()).decode()

        headers = {
            'Authorization' : 'Basic %s' % encoded_u,
            'Content-Type': 'application/json'
        }

        params = {
            'amount': final_charge_amount,
            'method': method,
            'orderId': order_id,
            'orderName': order_name,
            'successUrl': success_url,
            'failUrl': fail_url
        }

        data = {
            'order_name': order_name,
            'order_id': order_id,
            'method': method,
            'total_amount': total_amount,
            'spent_prepayment_amount': spent_prepayment_amount,
            'final_charge_amount': final_charge_amount,
            'requested_at': requested_at,
        }

        if order_name == '차량충전대금':
            serializer = ChargingPaymentRequestSerializer(data=data)

        else:
            serializer = PrepaymentRequestSerializer(data=data)

        response = requests.post(url, data=json.dumps(params), headers=headers)

        if response.status_code == 200:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, status=response['status'])

        """
        위의 로직을 따라 결제생성API와의 통신을 성공하고 'paymentKey'를 발급 받아야 결제승인API와의 통신이 가능합니다.
        발급 받은 'paymentKey'를 통해 새 params를 만들고 결제승인API URL로 새 요청을 전송하여 결제를 마무리하고
        응답 데이터를 바탕으로 후속조치를 진행합니다.
        예시는 아래와 같습니다.
        ```
        payment_key = response['paymentKey']
        url = "https://api.tosspayments.com/v1/payments/confirm"

        params = {
            'orderId': order_id,
            'amount': final_charge_amount,
            'paymentKey': payment_key
        }

        response = requests.post(url, data=json.dumps(params), headers=headers)
        ```

        예정사항: 응답 데이터(response)를 해체하여 DB에 저장
        응답 완료 후 리다이렉트 경로 지정
        상황 별 에러메시지 및 테스트코드 작성
        """