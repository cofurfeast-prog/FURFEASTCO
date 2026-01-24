from django.core.management.base import BaseCommand
from furfeast.models import Product
import json

class Command(BaseCommand):
    help = 'Fix image fields that are stored as JSON/dict from Supabase migration'

    def handle(self, *args, **options):
        self.stdout.write('Starting image data migration...')
        
        fixed_count = 0
        error_count = 0
        
        for product in Product.objects.all():
            try:
                # Check if image field is stored as string (JSON)
                if product.image and isinstance(product.image.name, str):
                    # Try to parse as JSON
                    try:
                        image_data = json.loads(product.image.name)
                        if isinstance(image_data, dict) and 'url' in image_data:
                            # Extract the actual file path from the URL
                            url = image_data['url']
                            # Extract path after bucket name
                            if 'storage.googleapis.com' in url:
                                path = url.split(f'{product._meta.app_label}/')[-1]
                            else:
                                path = url.split('/')[-1]
                            
                            # Update the field with just the path
                            product.image.name = path
                            product.save(update_fields=['image'])
                            fixed_count += 1
                            self.stdout.write(f'Fixed: {product.name} - {path}')
                    except (json.JSONDecodeError, ValueError):
                        # Not JSON, probably already correct
                        pass
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'Error with {product.name}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nMigration complete!\n'
            f'Fixed: {fixed_count} products\n'
            f'Errors: {error_count} products'
        ))
