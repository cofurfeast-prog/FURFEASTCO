@echo off
echo ============================================================
echo AUTOMATED CLEANUP FOR DEPLOYMENT
echo ============================================================
echo.
echo This script will:
echo   1. Delete all test files
echo   2. Delete all documentation files
echo   3. Delete helper scripts
echo   4. Show you what's left
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/4] Deleting test files...
if exist test_chat_persistence.py del /Q test_chat_persistence.py && echo   ✓ Deleted test_chat_persistence.py
if exist test_cleanup.py del /Q test_cleanup.py && echo   ✓ Deleted test_cleanup.py
if exist test_message_save.py del /Q test_message_save.py && echo   ✓ Deleted test_message_save.py
if exist health_check.py del /Q health_check.py && echo   ✓ Deleted health_check.py
if exist check_migration.py del /Q check_migration.py && echo   ✓ Deleted check_migration.py
if exist verify_migration.py del /Q verify_migration.py && echo   ✓ Deleted verify_migration.py

echo.
echo [2/4] Deleting helper scripts...
if exist apply_chatroom_updates.py del /Q apply_chatroom_updates.py && echo   ✓ Deleted apply_chatroom_updates.py
if exist update_chatroom_code.py del /Q update_chatroom_code.py && echo   ✓ Deleted update_chatroom_code.py
if exist deploy_check.bat del /Q deploy_check.bat && echo   ✓ Deleted deploy_check.bat
if exist deploy.bat del /Q deploy.bat && echo   ✓ Deleted deploy.bat
if exist start.sh del /Q start.sh && echo   ✓ Deleted start.sh

echo.
echo [3/4] Deleting documentation files...
if exist AUTO_CLEANUP_GUIDE.md del /Q AUTO_CLEANUP_GUIDE.md && echo   ✓ Deleted AUTO_CLEANUP_GUIDE.md
if exist CHAT_ARCHITECTURE_REFERENCE.md del /Q CHAT_ARCHITECTURE_REFERENCE.md && echo   ✓ Deleted CHAT_ARCHITECTURE_REFERENCE.md
if exist CHAT_DISAPPEARING_FIX.md del /Q CHAT_DISAPPEARING_FIX.md && echo   ✓ Deleted CHAT_DISAPPEARING_FIX.md
if exist CHAT_LIST_IMPROVEMENTS.md del /Q CHAT_LIST_IMPROVEMENTS.md && echo   ✓ Deleted CHAT_LIST_IMPROVEMENTS.md
if exist CHAT_PERSISTENCE_FIX.md del /Q CHAT_PERSISTENCE_FIX.md && echo   ✓ Deleted CHAT_PERSISTENCE_FIX.md
if exist CHATROOM_IMPLEMENTATION_GUIDE.md del /Q CHATROOM_IMPLEMENTATION_GUIDE.md && echo   ✓ Deleted CHATROOM_IMPLEMENTATION_GUIDE.md
if exist CHATROOM_MIGRATION_INSTRUCTIONS.md del /Q CHATROOM_MIGRATION_INSTRUCTIONS.md && echo   ✓ Deleted CHATROOM_MIGRATION_INSTRUCTIONS.md
if exist CLEANUP_QUICK_REFERENCE.md del /Q CLEANUP_QUICK_REFERENCE.md && echo   ✓ Deleted CLEANUP_QUICK_REFERENCE.md
if exist COMPLETE_CHAT_NOTIFICATION_SUMMARY.md del /Q COMPLETE_CHAT_NOTIFICATION_SUMMARY.md && echo   ✓ Deleted COMPLETE_CHAT_NOTIFICATION_SUMMARY.md
if exist complete_chat_system_for_claude.txt del /Q complete_chat_system_for_claude.txt && echo   ✓ Deleted complete_chat_system_for_claude.txt
if exist DEPLOYMENT.md del /Q DEPLOYMENT.md && echo   ✓ Deleted DEPLOYMENT.md
if exist MIGRATION_STEPS.md del /Q MIGRATION_STEPS.md && echo   ✓ Deleted MIGRATION_STEPS.md
if exist NEXT_STEPS.md del /Q NEXT_STEPS.md && echo   ✓ Deleted NEXT_STEPS.md
if exist NOTIFICATION_FIXES_SUMMARY.md del /Q NOTIFICATION_FIXES_SUMMARY.md && echo   ✓ Deleted NOTIFICATION_FIXES_SUMMARY.md
if exist QUICK_REFERENCE.md del /Q QUICK_REFERENCE.md && echo   ✓ Deleted QUICK_REFERENCE.md
if exist WHATSAPP_COMPARISON.md del /Q WHATSAPP_COMPARISON.md && echo   ✓ Deleted WHATSAPP_COMPARISON.md
if exist WHATSAPP_PERSISTENCE_VERIFICATION.md del /Q WHATSAPP_PERSISTENCE_VERIFICATION.md && echo   ✓ Deleted WHATSAPP_PERSISTENCE_VERIFICATION.md
if exist WHY_NO_CHATROOM_NEEDED.md del /Q WHY_NO_CHATROOM_NEEDED.md && echo   ✓ Deleted WHY_NO_CHATROOM_NEEDED.md
if exist CLEANUP_BEFORE_DEPLOY.md del /Q CLEANUP_BEFORE_DEPLOY.md && echo   ✓ Deleted CLEANUP_BEFORE_DEPLOY.md
if exist PRE_DEPLOYMENT_CHECKLIST.md del /Q PRE_DEPLOYMENT_CHECKLIST.md && echo   ✓ Deleted PRE_DEPLOYMENT_CHECKLIST.md

echo.
echo [4/4] Deleting backup files...
if exist furfeast\views_recovered.py del /Q furfeast\views_recovered.py && echo   ✓ Deleted views_recovered.py

echo.
echo ============================================================
echo ✅ CLEANUP COMPLETE!
echo ============================================================
echo.
echo Your project is now clean and ready for deployment.
echo.
echo Essential files kept:
echo   ✓ manage.py
echo   ✓ requirements.txt
echo   ✓ Dockerfile
echo   ✓ defang.yaml
echo   ✓ furfeast/ (app folder)
echo   ✓ FURFEASTCO/ (settings folder)
echo.
echo 🚀 Ready to deploy!
echo.
pause
