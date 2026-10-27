def normalize_url(url):
    if not url:
        return ""

    url = url.replace("https://ukplanningguide.co.uk", "")
    url = url.replace("//", "/")
    url = url.replace("index.html", "")

    if not url.startswith("/"):
        url = "/" + url

    if not url.endswith("/"):
        url += "/"

    return url


def canonical(base_url, path):
    base = base_url.rstrip("/")
    path = str(path).strip().strip("/")

    if not path:
        return f"{base}/"

    return f"{base}/{path}/"

import random
import hashlib


def page_rng(*args):
    """
    Deterministic random generator based on input args
    """
    seed_input = "|".join(str(a) for a in args)
    seed = int(hashlib.md5(seed_input.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)
    return random

import datetime

def get_month_year():
    return datetime.datetime.now().strftime("%B %Y")