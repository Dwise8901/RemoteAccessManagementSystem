import bcrypt
import pyotp


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def generate_mfa_secret():
    return pyotp.random_base32()


def verify_mfa_code(secret, code):
    if not secret:
        return False

    totp = pyotp.TOTP(secret)

    return totp.verify(
        code,
        valid_window=1
    )