@echo off
echo Starting migration of all files...
echo.

echo [1/35] Migrating: cd2eed8c-8b34-489b-bcfa-373f54e3da01_beautiful-dog-breed-list.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_1.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./cd2eed8c-8b34-489b-bcfa-373f54e3da01_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_1.tmp" "gs://furfeastco-media/cd2eed8c-8b34-489b-bcfa-373f54e3da01_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/cd2eed8c-8b34-489b-bcfa-373f54e3da01_beautiful-dog-breed-list.jpg"
del "temp_1.tmp"
echo [OK] Completed: cd2eed8c-8b34-489b-bcfa-373f54e3da01_beautiful-dog-breed-list.jpg
echo.

echo [2/35] Migrating: e4a819d3-0981-44cd-965e-d4c4bdfd0d58_a-greying-jowly-dog-with-soft-dark-eyes.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_2.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./e4a819d3-0981-44cd-965e-d4c4bdfd0d58_a-greying-jowly-dog-with-soft-dark-eyes.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_2.tmp" "gs://furfeastco-media/e4a819d3-0981-44cd-965e-d4c4bdfd0d58_a-greying-jowly-dog-with-soft-dark-eyes.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/e4a819d3-0981-44cd-965e-d4c4bdfd0d58_a-greying-jowly-dog-with-soft-dark-eyes.jpg"
del "temp_2.tmp"
echo [OK] Completed: e4a819d3-0981-44cd-965e-d4c4bdfd0d58_a-greying-jowly-dog-with-soft-dark-eyes.jpg
echo.

echo [3/35] Migrating: 23df26f3-6a6e-412d-9b97-d0e7134caffc_dogs_playing.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_3.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./23df26f3-6a6e-412d-9b97-d0e7134caffc_dogs_playing.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_3.tmp" "gs://furfeastco-media/23df26f3-6a6e-412d-9b97-d0e7134caffc_dogs_playing.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/23df26f3-6a6e-412d-9b97-d0e7134caffc_dogs_playing.jpg"
del "temp_3.tmp"
echo [OK] Completed: 23df26f3-6a6e-412d-9b97-d0e7134caffc_dogs_playing.jpg
echo.

echo [4/35] Migrating: 822e1d62-1286-4b7a-9e0d-54a1c183443b_Admin_Maina.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_4.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./822e1d62-1286-4b7a-9e0d-54a1c183443b_Admin_Maina.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_4.tmp" "gs://furfeastco-media/822e1d62-1286-4b7a-9e0d-54a1c183443b_Admin_Maina.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/822e1d62-1286-4b7a-9e0d-54a1c183443b_Admin_Maina.jpg"
del "temp_4.tmp"
echo [OK] Completed: 822e1d62-1286-4b7a-9e0d-54a1c183443b_Admin_Maina.jpg
echo.

echo [5/35] Migrating: b04618b7-71c7-47e8-a881-a617600bb671_dogs_playing.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_5.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./b04618b7-71c7-47e8-a881-a617600bb671_dogs_playing.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_5.tmp" "gs://furfeastco-media/b04618b7-71c7-47e8-a881-a617600bb671_dogs_playing.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/b04618b7-71c7-47e8-a881-a617600bb671_dogs_playing.jpg"
del "temp_5.tmp"
echo [OK] Completed: b04618b7-71c7-47e8-a881-a617600bb671_dogs_playing.jpg
echo.

echo [6/35] Migrating: 68a72214-41ac-457e-b097-d0fc24ec3e2a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_6.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./68a72214-41ac-457e-b097-d0fc24ec3e2a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_6.tmp" "gs://furfeastco-media/68a72214-41ac-457e-b097-d0fc24ec3e2a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/68a72214-41ac-457e-b097-d0fc24ec3e2a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
del "temp_6.tmp"
echo [OK] Completed: 68a72214-41ac-457e-b097-d0fc24ec3e2a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
echo.

echo [7/35] Migrating: 81a1441f-279d-454e-a66a-73a4efee3990_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_7.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./81a1441f-279d-454e-a66a-73a4efee3990_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_7.tmp" "gs://furfeastco-media/81a1441f-279d-454e-a66a-73a4efee3990_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/81a1441f-279d-454e-a66a-73a4efee3990_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
del "temp_7.tmp"
echo [OK] Completed: 81a1441f-279d-454e-a66a-73a4efee3990_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
echo.

echo [8/35] Migrating: d2f1899b-2dc9-4295-823d-2754d5c9b94a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_8.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./d2f1899b-2dc9-4295-823d-2754d5c9b94a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_8.tmp" "gs://furfeastco-media/d2f1899b-2dc9-4295-823d-2754d5c9b94a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/d2f1899b-2dc9-4295-823d-2754d5c9b94a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
del "temp_8.tmp"
echo [OK] Completed: d2f1899b-2dc9-4295-823d-2754d5c9b94a_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
echo.

echo [9/35] Migrating: e4286083-7081-4720-ac45-6a2bb411e77b_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_9.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./e4286083-7081-4720-ac45-6a2bb411e77b_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_9.tmp" "gs://furfeastco-media/e4286083-7081-4720-ac45-6a2bb411e77b_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/e4286083-7081-4720-ac45-6a2bb411e77b_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg"
del "temp_9.tmp"
echo [OK] Completed: e4286083-7081-4720-ac45-6a2bb411e77b_Screenshot_2026-01-18-15-15-02-002_com.android.chrome.jpg
echo.

echo [10/35] Migrating: desktop
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_10.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./desktop"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_10.tmp" "gs://furfeastco-media/desktop"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/desktop"
del "temp_10.tmp"
echo [OK] Completed: desktop
echo.

echo [11/35] Migrating: mobile
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_11.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./mobile"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_11.tmp" "gs://furfeastco-media/mobile"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/mobile"
del "temp_11.tmp"
echo [OK] Completed: mobile
echo.

echo [12/35] Migrating: 465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_12.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_12.tmp" "gs://furfeastco-media/465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg"
del "temp_12.tmp"
echo [OK] Completed: 465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg
echo.

echo [13/35] Migrating: 4ee70357-455b-48c8-bb44-ded3f20d0c22_dog_and_cat.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_13.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./4ee70357-455b-48c8-bb44-ded3f20d0c22_dog_and_cat.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_13.tmp" "gs://furfeastco-media/4ee70357-455b-48c8-bb44-ded3f20d0c22_dog_and_cat.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/4ee70357-455b-48c8-bb44-ded3f20d0c22_dog_and_cat.jpg"
del "temp_13.tmp"
echo [OK] Completed: 4ee70357-455b-48c8-bb44-ded3f20d0c22_dog_and_cat.jpg
echo.

echo [14/35] Migrating: 8c3bd030-04cf-4bfc-94fa-ba1cbdf4dcc1_ojV1dH.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_14.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./8c3bd030-04cf-4bfc-94fa-ba1cbdf4dcc1_ojV1dH.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_14.tmp" "gs://furfeastco-media/8c3bd030-04cf-4bfc-94fa-ba1cbdf4dcc1_ojV1dH.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/8c3bd030-04cf-4bfc-94fa-ba1cbdf4dcc1_ojV1dH.jpg"
del "temp_14.tmp"
echo [OK] Completed: 8c3bd030-04cf-4bfc-94fa-ba1cbdf4dcc1_ojV1dH.jpg
echo.

echo [15/35] Migrating: 946870e7-0bc9-47bd-b1ce-837f24135e2c_front-view-beautiful-dog-with-copy-space.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_15.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./946870e7-0bc9-47bd-b1ce-837f24135e2c_front-view-beautiful-dog-with-copy-space.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_15.tmp" "gs://furfeastco-media/946870e7-0bc9-47bd-b1ce-837f24135e2c_front-view-beautiful-dog-with-copy-space.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/946870e7-0bc9-47bd-b1ce-837f24135e2c_front-view-beautiful-dog-with-copy-space.jpg"
del "temp_15.tmp"
echo [OK] Completed: 946870e7-0bc9-47bd-b1ce-837f24135e2c_front-view-beautiful-dog-with-copy-space.jpg
echo.

echo [16/35] Migrating: c1c975e4-878b-4293-98e2-887a36b39585_cat_hddd.jpeg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_16.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./c1c975e4-878b-4293-98e2-887a36b39585_cat_hddd.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_16.tmp" "gs://furfeastco-media/c1c975e4-878b-4293-98e2-887a36b39585_cat_hddd.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/c1c975e4-878b-4293-98e2-887a36b39585_cat_hddd.jpeg"
del "temp_16.tmp"
echo [OK] Completed: c1c975e4-878b-4293-98e2-887a36b39585_cat_hddd.jpeg
echo.

echo [17/35] Migrating: fca2416f-c5a9-4d48-afd7-9b70101532d8_Cat.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_17.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./fca2416f-c5a9-4d48-afd7-9b70101532d8_Cat.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_17.tmp" "gs://furfeastco-media/fca2416f-c5a9-4d48-afd7-9b70101532d8_Cat.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/fca2416f-c5a9-4d48-afd7-9b70101532d8_Cat.jpg"
del "temp_17.tmp"
echo [OK] Completed: fca2416f-c5a9-4d48-afd7-9b70101532d8_Cat.jpg
echo.

echo [18/35] Migrating: 0238cb6a-4917-47b9-8f76-bf43b423b315_dog_leash.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_18.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./0238cb6a-4917-47b9-8f76-bf43b423b315_dog_leash.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_18.tmp" "gs://furfeastco-media/0238cb6a-4917-47b9-8f76-bf43b423b315_dog_leash.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/0238cb6a-4917-47b9-8f76-bf43b423b315_dog_leash.jpg"
del "temp_18.tmp"
echo [OK] Completed: 0238cb6a-4917-47b9-8f76-bf43b423b315_dog_leash.jpg
echo.

echo [19/35] Migrating: 06364022-3911-47a3-a980-eb46f259cad4_images.jpeg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_19.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./06364022-3911-47a3-a980-eb46f259cad4_images.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_19.tmp" "gs://furfeastco-media/06364022-3911-47a3-a980-eb46f259cad4_images.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/06364022-3911-47a3-a980-eb46f259cad4_images.jpeg"
del "temp_19.tmp"
echo [OK] Completed: 06364022-3911-47a3-a980-eb46f259cad4_images.jpeg
echo.

echo [20/35] Migrating: 38410c84-8d6c-436d-a16f-23661269df58_cat_bell.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_20.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./38410c84-8d6c-436d-a16f-23661269df58_cat_bell.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_20.tmp" "gs://furfeastco-media/38410c84-8d6c-436d-a16f-23661269df58_cat_bell.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/38410c84-8d6c-436d-a16f-23661269df58_cat_bell.jpg"
del "temp_20.tmp"
echo [OK] Completed: 38410c84-8d6c-436d-a16f-23661269df58_cat_bell.jpg
echo.

echo [21/35] Migrating: 7f950155-3803-485a-ad15-41a2a6550700_pedigree.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_21.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./7f950155-3803-485a-ad15-41a2a6550700_pedigree.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_21.tmp" "gs://furfeastco-media/7f950155-3803-485a-ad15-41a2a6550700_pedigree.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/7f950155-3803-485a-ad15-41a2a6550700_pedigree.jpg"
del "temp_21.tmp"
echo [OK] Completed: 7f950155-3803-485a-ad15-41a2a6550700_pedigree.jpg
echo.

echo [22/35] Migrating: 85e09328-6b80-4e9d-8006-ed33a4e1b14d_non-toxic-dog-toys-940x675.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_22.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./85e09328-6b80-4e9d-8006-ed33a4e1b14d_non-toxic-dog-toys-940x675.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_22.tmp" "gs://furfeastco-media/85e09328-6b80-4e9d-8006-ed33a4e1b14d_non-toxic-dog-toys-940x675.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/85e09328-6b80-4e9d-8006-ed33a4e1b14d_non-toxic-dog-toys-940x675.jpg"
del "temp_22.tmp"
echo [OK] Completed: 85e09328-6b80-4e9d-8006-ed33a4e1b14d_non-toxic-dog-toys-940x675.jpg
echo.

echo [23/35] Migrating: a04f50c4-5ab1-4879-98f3-5c8ce1e64b36_biralo_candy.webp
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_23.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./a04f50c4-5ab1-4879-98f3-5c8ce1e64b36_biralo_candy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_23.tmp" "gs://furfeastco-media/a04f50c4-5ab1-4879-98f3-5c8ce1e64b36_biralo_candy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/a04f50c4-5ab1-4879-98f3-5c8ce1e64b36_biralo_candy.webp"
del "temp_23.tmp"
echo [OK] Completed: a04f50c4-5ab1-4879-98f3-5c8ce1e64b36_biralo_candy.webp
echo.

echo [24/35] Migrating: a2256eee-13dc-4cc4-add8-527e0a2f024c_dog_toy.webp
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_24.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./a2256eee-13dc-4cc4-add8-527e0a2f024c_dog_toy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_24.tmp" "gs://furfeastco-media/a2256eee-13dc-4cc4-add8-527e0a2f024c_dog_toy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/a2256eee-13dc-4cc4-add8-527e0a2f024c_dog_toy.webp"
del "temp_24.tmp"
echo [OK] Completed: a2256eee-13dc-4cc4-add8-527e0a2f024c_dog_toy.webp
echo.

echo [25/35] Migrating: cb2b4a35-de0a-49e0-97d0-859390fb1727_hacker.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_25.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./cb2b4a35-de0a-49e0-97d0-859390fb1727_hacker.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_25.tmp" "gs://furfeastco-media/cb2b4a35-de0a-49e0-97d0-859390fb1727_hacker.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/cb2b4a35-de0a-49e0-97d0-859390fb1727_hacker.jpg"
del "temp_25.tmp"
echo [OK] Completed: cb2b4a35-de0a-49e0-97d0-859390fb1727_hacker.jpg
echo.

echo [26/35] Migrating: d5db5414-fe90-4559-82fa-f2ecab7cb449_Friskies_Cat.webp
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_26.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./d5db5414-fe90-4559-82fa-f2ecab7cb449_Friskies_Cat.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_26.tmp" "gs://furfeastco-media/d5db5414-fe90-4559-82fa-f2ecab7cb449_Friskies_Cat.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/d5db5414-fe90-4559-82fa-f2ecab7cb449_Friskies_Cat.webp"
del "temp_26.tmp"
echo [OK] Completed: d5db5414-fe90-4559-82fa-f2ecab7cb449_Friskies_Cat.webp
echo.

echo [27/35] Migrating: 0085fdfe-aba9-404a-a980-64cd3ddb5ef1_beautiful-dog-breed-list.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_27.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./0085fdfe-aba9-404a-a980-64cd3ddb5ef1_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_27.tmp" "gs://furfeastco-media/0085fdfe-aba9-404a-a980-64cd3ddb5ef1_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/0085fdfe-aba9-404a-a980-64cd3ddb5ef1_beautiful-dog-breed-list.jpg"
del "temp_27.tmp"
echo [OK] Completed: 0085fdfe-aba9-404a-a980-64cd3ddb5ef1_beautiful-dog-breed-list.jpg
echo.

echo [28/35] Migrating: 143e52a6-5a75-487e-a455-2dca600004c1_Messenger_creation_804988624904379.jpeg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_28.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./143e52a6-5a75-487e-a455-2dca600004c1_Messenger_creation_804988624904379.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_28.tmp" "gs://furfeastco-media/143e52a6-5a75-487e-a455-2dca600004c1_Messenger_creation_804988624904379.jpeg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/143e52a6-5a75-487e-a455-2dca600004c1_Messenger_creation_804988624904379.jpeg"
del "temp_28.tmp"
echo [OK] Completed: 143e52a6-5a75-487e-a455-2dca600004c1_Messenger_creation_804988624904379.jpeg
echo.

echo [29/35] Migrating: 17f89279-2308-4d5b-847d-716418fc98c4_Snapchat-2126040479.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_29.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./17f89279-2308-4d5b-847d-716418fc98c4_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_29.tmp" "gs://furfeastco-media/17f89279-2308-4d5b-847d-716418fc98c4_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/17f89279-2308-4d5b-847d-716418fc98c4_Snapchat-2126040479.jpg"
del "temp_29.tmp"
echo [OK] Completed: 17f89279-2308-4d5b-847d-716418fc98c4_Snapchat-2126040479.jpg
echo.

echo [30/35] Migrating: 321e8a03-c108-426e-857b-3dcd429dbe32_Snapchat-2126040479.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_30.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./321e8a03-c108-426e-857b-3dcd429dbe32_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_30.tmp" "gs://furfeastco-media/321e8a03-c108-426e-857b-3dcd429dbe32_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/321e8a03-c108-426e-857b-3dcd429dbe32_Snapchat-2126040479.jpg"
del "temp_30.tmp"
echo [OK] Completed: 321e8a03-c108-426e-857b-3dcd429dbe32_Snapchat-2126040479.jpg
echo.

echo [31/35] Migrating: 91175579-088d-41f7-a7c8-e17b996e88aa_hacker.webp
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_31.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./91175579-088d-41f7-a7c8-e17b996e88aa_hacker.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_31.tmp" "gs://furfeastco-media/91175579-088d-41f7-a7c8-e17b996e88aa_hacker.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/91175579-088d-41f7-a7c8-e17b996e88aa_hacker.webp"
del "temp_31.tmp"
echo [OK] Completed: 91175579-088d-41f7-a7c8-e17b996e88aa_hacker.webp
echo.

echo [32/35] Migrating: c1d517fb-56f8-478e-86af-c8cb1520f72b_Snapchat-2126040479.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_32.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./c1d517fb-56f8-478e-86af-c8cb1520f72b_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_32.tmp" "gs://furfeastco-media/c1d517fb-56f8-478e-86af-c8cb1520f72b_Snapchat-2126040479.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/c1d517fb-56f8-478e-86af-c8cb1520f72b_Snapchat-2126040479.jpg"
del "temp_32.tmp"
echo [OK] Completed: c1d517fb-56f8-478e-86af-c8cb1520f72b_Snapchat-2126040479.jpg
echo.

echo [33/35] Migrating: d8f4eec9-8c68-4234-a44e-6970a94e6b99_beautiful-dog-breed-list.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_33.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./d8f4eec9-8c68-4234-a44e-6970a94e6b99_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_33.tmp" "gs://furfeastco-media/d8f4eec9-8c68-4234-a44e-6970a94e6b99_beautiful-dog-breed-list.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/d8f4eec9-8c68-4234-a44e-6970a94e6b99_beautiful-dog-breed-list.jpg"
del "temp_33.tmp"
echo [OK] Completed: d8f4eec9-8c68-4234-a44e-6970a94e6b99_beautiful-dog-breed-list.jpg
echo.

echo [34/35] Migrating: e965103a-64a3-46a7-9172-f0ce81ba05c4_cutie.jpg
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_34.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./e965103a-64a3-46a7-9172-f0ce81ba05c4_cutie.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_34.tmp" "gs://furfeastco-media/e965103a-64a3-46a7-9172-f0ce81ba05c4_cutie.jpg"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/e965103a-64a3-46a7-9172-f0ce81ba05c4_cutie.jpg"
del "temp_34.tmp"
echo [OK] Completed: e965103a-64a3-46a7-9172-f0ce81ba05c4_cutie.jpg
echo.

echo [35/35] Migrating: f75e7c24-936e-4a08-8a4e-dff48ba02ec0_dog_toy.webp
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY" -o "temp_35.tmp" "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/FurfeastCo./f75e7c24-936e-4a08-8a4e-dff48ba02ec0_dog_toy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" cp "temp_35.tmp" "gs://furfeastco-media/f75e7c24-936e-4a08-8a4e-dff48ba02ec0_dog_toy.webp"
"C:\Users\LOQ\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd" acl ch -u AllUsers:R "gs://furfeastco-media/f75e7c24-936e-4a08-8a4e-dff48ba02ec0_dog_toy.webp"
del "temp_35.tmp"
echo [OK] Completed: f75e7c24-936e-4a08-8a4e-dff48ba02ec0_dog_toy.webp
echo.

echo [SUCCESS] Migration complete!
echo.
echo Your files are now available at:
echo https://storage.googleapis.com/furfeastco-media/
pause
