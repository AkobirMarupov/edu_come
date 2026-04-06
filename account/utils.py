import random
import requests

def send_eskiz_sms(phone_number):
    code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    
    auth_url = "http://notify.eskiz.uz/api/auth/login"
    auth_payload = {
        'email': 'imronhoja336@mail.ru',
        'password': 'ombeUIUC8szPawGi3TXgCjDXDD0uAIx2AmwLlX9M'
    }
    
    try:
        auth_response = requests.post(auth_url, data=auth_payload, timeout=10)
        token = auth_response.json()["data"]["token"]

        # 2. SMS yuborish
        send_url = "http://notify.eskiz.uz/api/message/sms/send"
        send_payload = {
            'mobile_phone': str(phone_number).replace('+', '').replace(' ', ''),
            'message': f"Envoy ilovasiga ro?yxatdan o?tish uchun tasdiqlash kodi: {code}",
            'from': '4546',
            'callback_url': 'http://0000.uz/test.php'
        }
        headers = {'Authorization': f"Bearer {token}"}
        
        requests.post(send_url, data=send_payload, headers=headers, timeout=10)
        return code
    except Exception as e:
        print(f"SMS yuborishda xatolik: {e}")
        return None