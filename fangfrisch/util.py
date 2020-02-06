import hashlib


def check_sha256(content, digest: str) -> bool:
    h = hashlib.new('sha256')
    h.update(content)
    return h.hexdigest() == digest


def represents_true(x: str) -> bool:
    return x and x.lower() in ['1', 'enabled', 'y', 'yes', 'true']


def write_binary(content, filename) -> bool:
    with open(filename, 'wb') as f:
        f.write(content)
    return True
