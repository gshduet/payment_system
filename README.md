# Cha** **ning 프로젝트
## 프로젝트 설명
체인**트닝이 개발 중인 충전 서비스는 선불 충전과 후불 결제가 모두 가능한 결제 시스템을 포함하고 있습니다.
다음 내용에 따라 결제 시스템의 데이터베이스와 백엔드 API 를 설계하고 문서를 작성 해 주세요.
  - 제출 양식과 형식에는 제한이 없습니다.

---
## 프로젝트 요구사항
- 사용자는 등록한 결제 수단으로 선불금 충전을 미리 하거나 하지 않을 수 있습니다.
- 사용자가 충전 서비스를 이용 완료 한 시점에 사용 금액은 자동으로 차감되거나 결제됩니다.
- 사용자는 무료 충전 쿠폰을 통해 일정 금액을 무료로 지급받을 수 있습니다.
- 결제 정보는 자사에 등록되며, 실제 결제가 이루어지는 로직은 PG 업체를 이용합니다.

- 리소스를 효율적으로 사용하고, 유지 보수가 용이한 방식이 무엇일지 고민해 보시고, 최대한 구체적으로 설명해주세요.
- 어떻게 하면 이러한 시스템을 구축할 수 있을지 아키텍쳐를 상세하게 설명해 주세요.

## 프로젝트 수행기간
23.04.03 ~ 23.04.07 (5일)

## 프로젝트 수행인원
백엔드 개발자 1인 - 권상현

## 사용된 기술스택
`Django 4.2`<br>
`Django-Rest-Framework 3.14.0`<br>
`DRF-SimpleJWT 5.2.2`<br>

---

## ERD
![title](https://user-images.githubusercontent.com/39396492/230606188-30cd65ab-8ee7-4567-8eeb-32efbfc492d4.png)

## 프로젝트 기능
* 사용자 회원가입, 로그인, 로그아웃
  * `JWT` 기반의 Token based Authentication System (DjangoRestframework-simpleJWT 기반)
  * [구현 사항 확인 링크](https://github.com/gshduet/payment_system/pull/1)
  * 테스트 결과
  ![title](https://user-images.githubusercontent.com/39396492/230064489-176f04fb-1556-4dcb-8682-9a63b184f2ea.png)
* 결제 시스템
  * 토스페이먼츠 결제 API를 통한 결제 시스템
  * 결제 과정에서 생성, 취득하는 데이터 저장 시스템 - 진행 중
  * 선불금 결제, 쿠폰 사용 등을 통한 선불금 충전 시스템 - 진행 중
  * [구현 사항 확인 링크](https://github.com/gshduet/payment_system/pull/3)

## API 명세서
  * 프로젝트 미완성에 따른 미첨부

## API 상세 명세서

| HTTP Method | URL | 기능 | Permission |
| --- | --- | --- | --- |
| `POST` | /users/signup | 유저 회원가입 | `AllowAny` |
| `POST` | /users/login | 유저 로그인 | `AllowAny` |
| `POST` | /users/logout | 로그아웃 | `IsAuthenticated` |
| `POST` | /payments | 결제창 | `IsAuthenticated` |
| `POST` | /payments/window (미정) | 사용자 카드 정보 입력 | `IsAuthenticated` |
| `POST` | /payments/success (미정) | 결제 완료 | `IsAuthenticated` |
| `POST` | /payments/fail (미정) | 결제 실패 | `IsAuthenticated` |

## 프로젝트 실행방법

1. 프로젝트를 클론 받는다.

    `git clone https://github.com/gshduet/payment_system.git`

2. 프로젝트는 `파이썬 3.10.6` 버전에서 구현됐으므로 해당 버전 이상의 Python을 필요로 한다. 버전에 맞는 가상환경을 설정하고 프로젝트의 루트 디렉토리로 이동한다.

    `cd payment_system` 

3. 프로젝트 구동에 필요한 패키지들을 다운로드한다. poetry 혹은 pip를 이용할 수 있다.

    `pip install -r requirements.txt`

4. 루트 디렉토리에 `.env`가 존재하는지 확인한다.
    * 실제 개발과정에서는 .gitignore에 추가하여 깃허브 레포지토리에 등록되어 있지 않았으나 제출 직전 업로드하였음

5. `.env`의 존재를 확인했다면 데이터베이스의 동기화를 위해 마이그레이트 한다.

    `python manage.py migrate` 혹은<br>
    `django-admin manage.py migrate`

6. `.env`의 존재를 확인했다면 서버를 구동한다.

    `python manage.py runserver 0:8000` 혹은 <br>
    `django-admin manage.py runserver 0:8000`

---

## 추후 구현 예정사항

1. 결제 시스템 완성 및 고도화
2. 각 기능 별 테스트
3. 간단한 클라이언트 사이드 구축
4. `swagger`를 통한 API 명세서 제작
5. 컨테이너화 및 배포

