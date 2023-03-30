from django.contrib.auth.models import User
from django import template
from django.utils.html import format_html
from blog.models import Post

register = template.Library()

#creating the custom filter to check and display author on html page.
@register.filter
def author_details(author,current_user):
    if isinstance(author, User):
        if author == current_user:
           return format_html("<strong>me</strong>")
        elif author.first_name and author.last_name:
            name = f"{author.first_name} {author.last_name}"
        else:
            name = f"{author.username}"
       #checking if the author has an assosiated email attached to his data.
        email_link = format_html('<a href="mailto:{}">{}</a>',author.email,name) if author.email else name
        return email_link
    return ""

#    -----------------------------------------------

# creating the autor_details with tag istead of filters
@register.simple_tag(takes_context=True)
def author_details_tag(context):
    current_user = context['request'].user
    post = context['post']
    author =post.author
    if author == current_user:
        return format_html("<strong>me</strong>")
    elif author.first_name and author.last_name:
        name =  f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"
    email_link = format_html('<a href="mailto:{}">{}</a>',author.email,name) if author.email else name
    return email_link

#    -----------------------------------------------

# creating the tag for the row div
@register.simple_tag
def row(extra_classes=''):
    return format_html('<div class = "row {}">',extra_classes)

@register.simple_tag
def endrow():
    return format_html('</div>')

#    -----------------------------------------------

# creating the tag for the column div
@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")

#    -----------------------------------------------

#writing an inclusive tag function for recent posts
@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {'title':'Recent Posts','posts':posts}