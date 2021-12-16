def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)", "x-user-language": "es", "accept-encoding": "gzip", "content-length": "0",
          "host_api": "test-api.lanadigital.mx", "x-app-name": "LanaDigital", "content-type": "application/json",
        "x-app-type": "10090001", "x-app-version": "1.0.0", "x-app-no": "208", "x-auth-token": 'Bearer ' + token }
    return head
def head_token2(token):
    head={"user-agent": "Dart/2.12 (dart:io)", "x-user-language": "es", "accept-encoding": "gzip", "content-length": "63",
          "host_api": "test-action.lanadigital.mx", "x-app-name": "LanaDigital", "content-type": "application/json",
        "x-app-type": "10090001", "x-app-version": "1.0.0", "x-app-no": "208", "x-auth-token": 'Bearer ' + token }
    return head
def head_token_kyc(token):
    head={"user-agent": "Dart/2.12 (dart:io)", "x-user-language": "es", "accept-encoding": "gzip", "content-length": "63",
          "host_api": "test-api.lanadigital.mx", "x-app-name": "LanaDigital", "content-type": "multipart/form-data; boundary=--dioBoundary&Happycoding-1538342764",
        "x-app-type": "10090001", "x-app-version": "1.0.0", "x-app-no": "208", "x-auth-token": 'Bearer ' + token }
    return head
def head_token_payment(token):
    head={"user-agent": "okhttp/4.9.1", "x-user-language": "", "accept-encoding": "gzip", "content-length": "0", "host_api": "test-api.lanadigital.mx", "x-app-name": "LanaDigital", "content-type": "application/json",
          "x-app-type": "10090001", "x-app-version": "1.0.0", "x-app-no": "208", "x-auth-token": 'Bearer ' + token}
    return head
def head_token_f(token):
    head = {"user-agent": "okhttp/4.9.1", "x-user-language": "", "accept-encoding": "gzip", "content-length": "828819",
            "host_api": "test-api.lanadigital.mx", "x-app-name": "LanaDigital", "content-type": "multipart/form-data; boundary=1a0e643e-b2e6-44f3-a8a4-94eb7f5eb4f4",
            "x-app-type": "10090001", "x-app-version": "1.0.0", "x-app-no": "208", "x-auth-token": 'Bearer ' + token}
    return head
