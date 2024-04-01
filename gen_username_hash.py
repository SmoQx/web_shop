from hashlib import md5


def gen_username_hash(username: str) -> str:
    hash = md5()
    hash.update(username.encode("utf-8"))

    return str(hash.hexdigest())


if __name__ == "__main__":
    email_text = "address@gmail.com"
    print(gen_username_hash(email_text))
