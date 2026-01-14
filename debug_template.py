#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile
from django.template import Template, Context
from django.template.loader import get_template

def debug_template_rendering():
    print("=== TEMPLATE RENDERING DEBUG ===")
    
    # Get the user with profile picture
    user = User.objects.get(username='nishakatuwal.77')
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    
    # Check profile
    try:
        profile = user.profile
        print(f"Profile exists: YES")
        print(f"Profile picture field: {profile.profile_picture}")
        print(f"Profile picture name: {profile.profile_picture.name if profile.profile_picture else 'None'}")
        print(f"Profile picture URL: {profile.profile_picture.url if profile.profile_picture else 'None'}")
        print(f"Profile picture bool: {bool(profile.profile_picture)}")
    except UserProfile.DoesNotExist:
        print(f"Profile exists: NO")
        return
    
    # Test the exact template logic
    print(f"\n=== TEMPLATE CONDITION TESTS ===")
    print(f"user.profile: {user.profile}")
    print(f"user.profile exists: {hasattr(user, 'profile')}")
    print(f"user.profile.profile_picture: {user.profile.profile_picture}")
    print(f"bool(user.profile.profile_picture): {bool(user.profile.profile_picture)}")
    
    # Test the template condition
    condition1 = user.profile and user.profile.profile_picture
    print(f"Condition (user.profile and user.profile.profile_picture): {condition1}")
    
    # Test template rendering
    print(f"\n=== TEMPLATE RENDERING TEST ===")
    template_code = """
    {% if user.profile and user.profile.profile_picture %}
        <img src="{{ user.profile.profile_picture.url }}" alt="Profile" class="w-full h-full object-cover">
    {% else %}
        {{ user.first_name|make_list|first|upper }}{{ user.last_name|make_list|first|upper }}
    {% endif %}
    """
    
    template = Template(template_code)
    context = Context({'user': user})
    rendered = template.render(context)
    print(f"Rendered template: {rendered.strip()}")
    
    # Test initials
    print(f"\n=== INITIALS TEST ===")
    first_initial = user.first_name[0].upper() if user.first_name else ''
    last_initial = user.last_name[0].upper() if user.last_name else ''
    initials = f"{first_initial}{last_initial}"
    print(f"First name: '{user.first_name}'")
    print(f"Last name: '{user.last_name}'")
    print(f"First initial: '{first_initial}'")
    print(f"Last initial: '{last_initial}'")
    print(f"Combined initials: '{initials}'")
    
    # Test Django template filters
    print(f"\n=== DJANGO TEMPLATE FILTER TEST ===")
    template_initials = Template("{{ user.first_name|make_list|first|upper }}{{ user.last_name|make_list|first|upper }}")
    rendered_initials = template_initials.render(context)
    print(f"Template rendered initials: '{rendered_initials}'")

if __name__ == "__main__":
    debug_template_rendering()