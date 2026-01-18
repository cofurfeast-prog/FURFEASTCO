@echo off
echo ============================================================
echo CLEANUP BEFORE DEPLOYMENT
echo ============================================================
echo.
echo This will delete test files and documentation.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Deleting test files...
del /Q test_chat_persistence.py 2>nul
del /Q test_cleanup.py 2>nul
del /Q test_message_save.py 2>nul
del /Q health_check.py 2>nul
del /Q check_migration.py 2>nul
del /Q verify_migration.py 2>nul

echo Deleting migration helper scripts...
del /Q apply_chatroom_updates.py 2>nul
del /Q update_chatroom_code.py 2>nul

echo Deleting documentation files...
del /Q AUTO_CLEANUP_GUIDE.md 2>nul
del /Q CHAT_ARCHITECTURE_REFERENCE.md 2>nul
del /Q CHAT_DISAPPEARING_FIX.md 2>nul
del /Q CHAT_LIST_IMPROVEMENTS.md 2>nul
del /Q CHAT_PERSISTENCE_FIX.md 2>nul
del /Q CHATROOM_IMPLEMENTATION_GUIDE.md 2>nul
del /Q CHATROOM_MIGRATION_INSTRUCTIONS.md 2>nul
del /Q CLEANUP_QUICK_REFERENCE.md 2>nul
del /Q COMPLETE_CHAT_NOTIFICATION_SUMMARY.md 2>nul
del /Q complete_chat_system_for_claude.txt 2>nul
del /Q DEPLOYMENT.md 2>nul
del /Q MIGRATION_STEPS.md 2>nul
del /Q NEXT_STEPS.md 2>nul
del /Q NOTIFICATION_FIXES_SUMMARY.md 2>nul
del /Q QUICK_REFERENCE.md 2>nul
del /Q WHATSAPP_COMPARISON.md 2>nul
del /Q WHATSAPP_PERSISTENCE_VERIFICATION.md 2>nul
del /Q WHY_NO_CHATROOM_NEEDED.md 2>nul

echo Deleting backup files...
del /Q furfeast\views_recovered.py 2>nul

echo Deleting old deployment scripts...
del /Q deploy_check.bat 2>nul
del /Q deploy.bat 2>nul
del /Q start.sh 2>nul

echo.
echo ============================================================
echo ✅ CLEANUP COMPLETE!
echo ============================================================
echo.
echo Deleted files:
echo   - Test scripts (6 files)
echo   - Migration helpers (2 files)
echo   - Documentation (18 files)
echo   - Backup files (1 file)
echo   - Old deployment scripts (3 files)
echo.
echo Your codebase is now clean and ready for deployment!
echo.
echo Next steps:
echo   1. Review remaining files
echo   2. Commit to git
echo   3. Deploy to Defang
echo.
pause
