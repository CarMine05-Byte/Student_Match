import hashlib
import hmac
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "data" / "corsi_laurea.txt"


def hash_password(password):
    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + "$" + digest.hex()


def verify_password(password, stored_password):
    if not isinstance(password, str) or not isinstance(stored_password, str):
        return False

    if not password or not stored_password:
        return False

    try:
        salt_hex, digest_hex = stored_password.split("$")

        salt = bytes.fromhex(salt_hex)

        new_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return hmac.compare_digest(new_digest.hex(), digest_hex)

    except ValueError:
        return False


def get_corsi_laurea():
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
