import re
from collections import defaultdict

LINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")

def extract_links(text: str):
    return LINK_PATTERN.findall(text)
