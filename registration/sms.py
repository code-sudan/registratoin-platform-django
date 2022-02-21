def send_sms(phone_number, sms_to_send, name = None, program = None):
    import http.client
    import urllib.parse


    
    API_KEY = "Z2lwbXVHcGtNdG5HRWlLY0lpY2w="
    SENDER_ID = "CodeSudan"


    if sms_to_send == "registration_sms":
        sms_to_encode = "مرحبا بك في عائلة كود_ سودان، نتمنى لك رحلة تعليمية ممتعة مع برامجنا الأونلاين"
    elif sms_to_send == "details_completed" and name != None:
        sms_to_encode = f"مرحبا {name} في عائلة كود_ سودان، نتمنى لك رحلة تعليمية ممتعة مع برامجنا الأونلاين، تم حفظ بياناتك."
    elif sms_to_send == "program_registration_sms" and program != None:
        sms_to_encode = f"أنت في طريقك للتسجيل لبرنامج {program} قم بدفع رسوم البرنامج لحفظ مقعدك"
    elif sms_to_send == "program_enrollment_sms" and program != None:
        sms_to_encode = f"تم إكمال تسجيلك لبرنامج {program}، نتمنى لكم رحلة تعليمية ممتعة"
    else:
        return 0





    sms_body = urllib.parse.quote_plus(sms_to_encode)
    
    conn = http.client.HTTPSConnection("mazinhost.com")
    payload = ''
    headers = {
    'Cookie': 'laravel_session=eyJpdiI6IlNrdXBkODlyRkNXTEY1ZGVkMkNCMEE9PSIsInZhbHVlIjoiY0VBVEJOcHRCdENLTnZTMW9FVldKdFQyNER3ajQwdzZzTW1NSWd6RFRVTXhxcVplWTZrSDQ3ZmhYWTdYQnN4NXZ0czZKbkQ3amVLbEZJMEhweFl1cnc9PSIsIm1hYyI6IjEzZjFhODYzOWUwYzgyNWNkMTFmNjlkM2RmNDVhMzdjYmM4Y2U2ZTlkYTNmNWZkYmUwYmZhNjM1ZTgxZmFmN2QifQ%3D%3D'
    }

    conn.request("POST", f"/smsv1/sms/api?action=send-sms&api_key=Z2lwbXVHcGtNdG5HRWlLY0lpY2w=&to={phone_number}&from=CodeSudan&sms={sms_body}&unicode=1", payload, headers)
    res = conn.getresponse()
    data = res.read()