import hashlib
import argon2


def gen_password_hash(user_password: str) -> str:
    salt = "asdf" 
    hasher = argon2.PasswordHasher()
    hashed = hasher.hash(user_password + salt)

    return str(hashed)


if __name__ == "__main__":
    pass_word = "asdf"
    print(gen_password_hash(pass_word))
