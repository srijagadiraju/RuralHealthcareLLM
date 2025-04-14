import re
from bs4 import BeautifulSoup


def clean_text(text):
    """Remove HTML tags, extra whitespace, and lowercase the text."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()
