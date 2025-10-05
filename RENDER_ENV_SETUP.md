# Render Environment Variables Setup

## 🚨 URGENT - Add these to Render NOW!

Go to: **Render Dashboard → Your Service → Environment**

Add these **2 variables**:

### 1. SUPABASE_URL
```
Your Supabase project URL
Example: https://xxxxxxxxxxxxx.supabase.co
```

### 2. SUPABASE_KEY
```
Your Supabase anon/public key
Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Where to find Supabase credentials?

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Click **Settings** → **API**
4. Copy:
   - **Project URL** → Use for `SUPABASE_URL`
   - **anon public** key → Use for `SUPABASE_KEY`

---

## After adding environment variables:

1. Render will **automatically redeploy**
2. Wait 2-3 minutes for deployment
3. Try uploading PDF again
4. Should work! ✅

---

## Note:
- OpenRouter API keys are already in the code
- You ONLY need to add Supabase credentials
- Without these, backend returns 422 error

---

## Quick Test:
After adding env vars, visit:
```
https://global-hackathon-v1-neet.onrender.com/health
```

Should return: `{"status": "healthy"}`
