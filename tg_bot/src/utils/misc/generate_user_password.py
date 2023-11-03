import random
import string


def generate_user_password(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for _ in range(length))
    return password
