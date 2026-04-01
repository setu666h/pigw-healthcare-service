from cryptography.fernet import Fernet

# Hardcoded key (generated using Fernet.generate_key())
# In production, store this in environment variables
KEY = b'Lib8ceP3jAyv4LIUsGgOP4697xiv6xt3BCpVep3B4Ww='

cipher = Fernet(KEY)


def encrypt_data(data: str) -> bytes:
    """
    Encrypt sensitive data
    """
    if not data:
        return None
    return cipher.encrypt(data.encode())


def decrypt_data(data) -> str:
    """
    Decrypt sensitive data
    """
    if not data:
        return None

    if isinstance(data, memoryview):
        data = data.tobytes()

    return cipher.decrypt(data).decode()


def mask_ssn(ssn: str) -> str:
    """
    Mask
    """
    if not ssn or len(ssn) < 4:
        return "****"
    return "***-**-" + ssn[-4:]