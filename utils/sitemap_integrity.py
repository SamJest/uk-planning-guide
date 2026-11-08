"""Validate emitted sitemap targets before writing XML; no URL rewrites."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('name', '').lower() in {'robots', 'googlebot'}:
            self.robots.extend(attrs.get('content', '').lower().replace(',', ' ').split())


def validate_targets(urls, output, base_url):
    output = Path(output).resolve()
    origin = urlsplit(base_url)
    seen = set()
    for url in urls:
        parsed = urlsplit(url)
        if (parsed.scheme != origin.scheme or parsed.netloc != origin.netloc
                or parsed.query or parsed.fragment or not parsed.path.endswith('/')):
            raise ValueError(f'Malformed sitemap URL: {url}')
        if url in seen:
            raise ValueError(f'Duplicate URL detected: {url}')
        seen.add(url)
        path = (output / unquote(parsed.path).strip('/') / 'index.html').resolve()
        if not path.is_relative_to(output) or not path.is_file():
            raise ValueError(f'Sitemap target is absent or outside output: {url}')
        metadata = Metadata()
        metadata.feed(path.read_text(encoding='utf-8'))
        if metadata.canonicals != [url]:
            raise ValueError(f'Sitemap target must have one matching canonical: {url}')
        if 'noindex' in metadata.robots or 'none' in metadata.robots:
            raise ValueError(f'Sitemap target is noindex: {url}')
