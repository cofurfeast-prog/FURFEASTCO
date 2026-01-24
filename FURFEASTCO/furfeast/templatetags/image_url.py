from django import template

register = template.Library()

@register.filter
def get_image_url(image_field):
    """
    Safely get image URL from either ImageFieldFile or dict (Supabase legacy format).
    """
    if not image_field:
        return ''
    
    # If it's a dict (old Supabase format)
    if isinstance(image_field, dict):
        return image_field.get('url', '')
    
    # If it's an ImageFieldFile (GCS format)
    if hasattr(image_field, 'url'):
        try:
            return image_field.url
        except:
            return ''
    
    # If it's a string path
    if isinstance(image_field, str):
        return image_field
    
    return ''
