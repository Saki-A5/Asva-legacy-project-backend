import secrets
import string


def generate_reference_code(prefix: str = "ASV-", length: int = 5) -> str:
    alphabet = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}{code}"

