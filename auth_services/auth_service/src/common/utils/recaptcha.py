import requests
from django.conf import settings

def verify_recaptcha(token):
    # print("===== RECAPTCHA CHECK START =====")
    # print("Received token:", token)
    #
    # if not token:
    #     print("ERROR: Missing token")
    #     return False
    #
    # if not settings.RECAPTCHA_SECRET_KEY:
    #     print("ERROR: Missing SECRET KEY in settings")
    #     return False
    #
    # url = "https://www.google.com/recaptcha/api/siteverify"
    # data = {
    #     'secret': settings.RECAPTCHA_SECRET_KEY,
    #     'response': token
    # }
    #
    # try:
    #     resp = requests.post(url, data=data, timeout=10)  # Increased timeout
    #     result = resp.json()
    #
    #     print("Google API Response:", result)   # DEBUG HERE
    #
    #     # For reCAPTCHA v2, we only check success
    #     # For reCAPTCHA v3, we check success AND score >= 0.5
    #     if result.get('success'):
    #         # If score is present (v3), check it; otherwise (v2) just return True
    #         score = result.get("score")
    #         if score is not None:
    #             if score >= 0.5:
    #                 print("RECAPTCHA VERIFIED: TRUE (v3)")
    #                 return True
    #             else:
    #                 print(f"RECAPTCHA VERIFIED: FALSE (v3 score {score} < 0.5)")
    #                 return False
    #         else:
    #             print("RECAPTCHA VERIFIED: TRUE (v2)")
    #             return True
    #     else:
    #         print("RECAPTCHA VERIFIED: FALSE (API returned success=False)")
    #         print("Error codes:", result.get('error-codes', []))
    #         return False
    #
    # except Exception as e:
    #     print("RECAPTCHA ERROR:", e)
    #     return False
    
    # For now, always return True to bypass reCAPTCHA
    return True
