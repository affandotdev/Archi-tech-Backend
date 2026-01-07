import pyotp


def gen_mfa_secret():
    return pyotp.random_base32()


def get_totp_uri(secret, username, issuer_name="ArchiTech"):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)


def verify_totp_token(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
