import hashlib


def gen_password_hash(user_password: str) -> str:
    hasher = hashlib.sha256()
    salt = "asdf" 
    user_password = user_password + salt
    hasher.update(user_password.encode("utf-8"))
    user_password = hasher.hexdigest()

    return str(user_password)


if __name__ == "__main__":
    pass_word = "asdf"
    print(gen_password_hash(pass_word))
