import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generators.faq_pages import generate_faq_pages

if __name__ == "__main__":
    generate_faq_pages()