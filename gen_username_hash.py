import argon2


def gen_username_hash(username: str) -> str:
    hasher = argon2.PasswordHasher()
    hashed = hasher.hash(username)

    return str(hashed)


if __name__ == "__main__":
    email_text = "address@gmail.com"
    print(gen_username_hash(email_text))
