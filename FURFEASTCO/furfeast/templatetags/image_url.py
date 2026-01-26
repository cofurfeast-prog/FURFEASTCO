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
    
    # If it's a string path
    if isinstance(image_field, str):
        return image_field
    
    # If it's an ImageFieldFile (GCS format) - check type name to avoid triggering property
    if type(image_field).__name__ == 'ImageFieldFile' or type(image_field).__name__ == 'FieldFile':
        try:
            return image_field.url
        except Exception as e:
            # If GCS fails, return empty string
            return ''
    
    return ''
