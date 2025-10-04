# 🚀 Deployment Guide

## Backend (Render) - Environment Variables

Add these to your Render service:

```env
# Supabase (Get from your Supabase project)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# OpenRouter AI API Keys (Already in code, but can override)
# These are already configured in the code from prompt.md
# No need to add unless you want to override

# Optional
FRONTEND_URL=https://global-hackathon-v1-olive.vercel.app
```

## Frontend (Vercel) - Environment Variables

Add these to your Vercel project:

```env
NEXT_PUBLIC_API_URL=https://global-hackathon-v1-neet.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Supabase Setup

1. Go to your Supabase project dashboard
2. Click on "SQL Editor"
3. Copy the contents of `backend/supabase_schema.sql`
4. Paste and run in SQL Editor
5. Go to "Storage" and create a bucket named `pitch-decks` (make it public)

## That's it!

Both frontend and backend will auto-deploy when you push to GitHub.

### Test Your Deployment

1. Upload a PDF pitch deck at your Vercel URL
2. Set filters (sector, stage, etc.)
3. Click "Analyze"
4. Watch real-time progress
5. Get REAL AI-powered results (no mocks!)

---

**Note**: First cold start on Render takes 30-60 seconds. Subsequent requests are fast.
