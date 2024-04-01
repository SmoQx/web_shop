import hashlib


def gen_password_hash(user_password: str) -> str:
    md5_hasher = hashlib.md5()
    salt = "asdf" 
    user_password = user_password + salt
    md5_hasher.update(user_password.encode("utf-8"))
    user_password = md5_hasher.hexdigest()

    return str(user_password)


if __name__ == "__main__":
    pass_word = "asdf"
    print(gen_password_hash(pass_word))
