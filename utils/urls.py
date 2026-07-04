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

def safe_link(url: str, text: str) -> str:
    url = normalize_url(url)
    return f'<a href="{url}">{text}</a>'