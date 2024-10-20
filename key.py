import secrets

def key():
    return secrets.token_hex(16)

if __name__ == "__main__":
    print(key())
