from django import template

register = template.Library()

@register.filter
def safe_image_url(image_field):
    """Safely get image URL, return empty string if fails"""
    try:
        if image_field:
            return image_field.url
    except:
        pass
    return ""
