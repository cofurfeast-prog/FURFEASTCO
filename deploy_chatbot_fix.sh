#!/bin/bash

# FurFeast Chatbot Fix Deployment Script
echo "🤖 Deploying FurFeast Chatbot Fixes..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations (if any)
echo "🗄️ Running migrations..."
python manage.py migrate

# Test the chatbot endpoints
echo "🧪 Testing chatbot endpoints..."

# Test basic chatbot endpoint
echo "Testing /api/chatbot/message/..."
curl -X POST http://localhost:8080/api/chatbot/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}' \
  --silent --output /dev/null --write-out "Status: %{http_code}\n"

# Test chatbot test endpoint
echo "Testing /api/chatbot/test/message/..."
curl -X POST http://localhost:8080/api/chatbot/test/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What products do you have?"}' \
  --silent --output /dev/null --write-out "Status: %{http_code}\n"

echo "✅ Deployment complete!"
echo ""
echo "🔗 Test URLs:"
echo "   • Chatbot Test Page: http://localhost:8080/chatbot/test/"
echo "   • Main Site: http://localhost:8080/"
echo ""
echo "📱 Mobile Testing Instructions:"
echo "   1. Open the test page on your phone"
echo "   2. Check if the chatbot button is visible"
echo "   3. Test opening/closing the chat modal"
echo "   4. Send test messages"
echo "   5. Check responsiveness in different orientations"
echo ""
echo "🐛 Issues Fixed:"
echo "   ✓ Chatbot button visibility across all devices"
echo "   ✓ Proper z-index to stay above other elements"
echo "   ✓ Responsive design for mobile, tablet, and desktop"
echo "   ✓ Better touch targets for mobile devices"
echo "   ✓ Improved modal positioning and sizing"
echo "   ✓ Enhanced accessibility features"
echo "   ✓ Cross-browser compatibility"
echo "   ✓ Comprehensive testing suite"