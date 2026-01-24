from django.core.management.base import BaseCommand
from furfeast.models import ChatBotIntent

class Command(BaseCommand):
    help = 'Setup default chatbot intents'

    def handle(self, *args, **options):
        intents = [
            {
                'name': 'product_search',
                'keywords': ['search', 'find', 'looking for', 'need', 'want'],
                'response_template': 'You can search for products using our search bar on the website, or tell me what specific product you\'re looking for and I\'ll help you find it! 🔍',
                'priority': 10
            },
            {
                'name': 'delivery_time',
                'keywords': ['how long', 'delivery time', 'when will', 'how fast'],
                'response_template': '🚚 Delivery Times:\n• Kathmandu Valley: 2-3 days\n• Major cities: 3-5 days\n• Remote areas: 5-7 days\n\nWe use reliable courier services for safe delivery!',
                'priority': 8
            },
            {
                'name': 'return_policy',
                'keywords': ['return', 'refund', 'exchange', 'money back'],
                'response_template': '↩️ Return Policy:\n• 7-day return policy for unopened items\n• Full refund for damaged products\n• Contact us at cofurfeast@gmail.com for returns\n• We prioritize customer satisfaction!',
                'priority': 7
            },
            {
                'name': 'bulk_order',
                'keywords': ['bulk', 'wholesale', 'large order', 'many items'],
                'response_template': '📦 Bulk Orders:\n• Special discounts for bulk purchases\n• Contact us at cofurfeast@gmail.com for wholesale pricing\n• Perfect for pet shops, shelters, and breeders\n• Custom delivery arrangements available',
                'priority': 6
            },
            {
                'name': 'pet_advice',
                'keywords': ['advice', 'help', 'recommend', 'best food', 'which food'],
                'response_template': '🐾 Pet Care Advice:\n• Choose age-appropriate food (puppy/kitten vs adult)\n• Consider your pet\'s size and activity level\n• Look for high-quality protein as first ingredient\n• Consult your vet for specific dietary needs\n\nNeed specific recommendations? Tell me about your pet!',
                'priority': 5
            }
        ]

        for intent_data in intents:
            intent, created = ChatBotIntent.objects.get_or_create(
                name=intent_data['name'],
                defaults={
                    'keywords': intent_data['keywords'],
                    'response_template': intent_data['response_template'],
                    'priority': intent_data['priority'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created intent: {intent.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Intent already exists: {intent.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully setup chatbot intents!')
        )