@echo off
echo Starting FurFeast deployment to Defang...

echo.
echo Step 1: Building and deploying with Defang...
defang compose up

echo.
echo Step 2: Checking deployment status...
defang ps

echo.
echo Deployment complete! 
echo Your app should be available at: https://taj8z613n2jd7-furfeastco.prod2.defang.dev
echo Health check: https://taj8z613n2jd7-furfeastco.prod2.defang.dev/health/

pause