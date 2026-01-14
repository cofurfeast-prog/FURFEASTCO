# FurFeast Deployment Instructions

## 1. Update Supabase Credentials
Edit compose.yaml and replace these values with your actual Supabase credentials:

- DB_USER: "postgres.your-project-ref" 
- DB_PASSWORD: "your-supabase-password"
- DB_HOST: "aws-0-region.pooler.supabase.com"
- SECRET_KEY: "your-django-secret-key"

## 2. Get your Supabase credentials:
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Settings > Database
4. Copy the connection details

## 3. Deploy with Defang:
```bash
defang up
```

## 4. Your app will be available at the URL provided by Defang