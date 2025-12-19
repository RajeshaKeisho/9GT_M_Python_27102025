from django import template
import re
from datetime import datetime

register = template.Library()

@register.filter
def format_date(value):
    return datetime.strptime(value, "%Y-%m-%d").strftime("%B %d, %Y")

@register.filter
def truncate_words(value, word_count):
    words = value.split()[:word_count]
    return " ".join(words) + "..." if len(value.split()) > word_count else value

@register.filter
def highlight_word(value, word):
    highlighted = re.sub(f'({word})', r'<strong style="color:red;">\1</strong>', value, flags=re.IGNORECASE)
    return highlighted


@register.filter
def reverse_text(value):
    """Reverse the entire text."""
    return value[::-1]

@register.filter
def uppercase_first(value):
    """Capitalize only the first word of a sentence."""
    return value[0].upper() + value[1:] if value else ""
