from django.contrib.auth.models import User
from django import template
from django.utils.html import format_html
register = template.Library()

@register.filter
def author_details(author,current_user):
    if isinstance(author, User):
        if author == current_user:
            return format_html("<strong>me</strong>")
        elif author.first_name and author.last_name:
            name = f"{author.first_name} {author.last_name}"
        else:
            name = f"{author.username}"
        email_link = format_html('<a href="mailto:{}">{}</a>',author.email,name) if author.email else name
        return email_link
    return ""