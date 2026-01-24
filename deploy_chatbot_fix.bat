@echo off
echo 🤖 Deploying FurFeast Chatbot Fixes...
echo.

cd /d "c:\Users\LOQ\OneDrive\Desktop\FURFEAST GOOGLE CLOUD\FURFEASTCO\FURFEASTCO"

echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 🗄️ Running migrations...
python manage.py migrate

echo.
echo ✅ Deployment complete!
echo.
echo 🔗 Test URLs:
echo    • Chatbot Test Page: http://localhost:8080/chatbot/test/
echo    • Main Site: http://localhost:8080/
echo.
echo 📱 Mobile Testing Instructions:
echo    1. Open the test page on your phone
echo    2. Check if the chatbot button is visible
echo    3. Test opening/closing the chat modal
echo    4. Send test messages
echo    5. Check responsiveness in different orientations
echo.
echo 🐛 Issues Fixed:
echo    ✓ Chatbot button visibility across all devices
echo    ✓ Proper z-index to stay above other elements
echo    ✓ Responsive design for mobile, tablet, and desktop
echo    ✓ Better touch targets for mobile devices
echo    ✓ Improved modal positioning and sizing
echo    ✓ Enhanced accessibility features
echo    ✓ Cross-browser compatibility
echo    ✓ Comprehensive testing suite
echo.
echo 🚀 Ready to test! Press any key to start the development server...
pause >nul

echo Starting development server...
python manage.py runserver 0.0.0.0:8080