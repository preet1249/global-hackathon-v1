# Frontend - VC Multi-Agent Platform

Next.js frontend for AI-powered startup due diligence platform.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📦 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn UI
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Database**: Supabase (Client)

## 🌐 Deploy to Vercel

### Option 1: Via Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Select the `frontend` folder as root directory
4. Add environment variables (see `.env.example`)
5. Click Deploy

### Option 2: Via Vercel CLI
```bash
npm i -g vercel
vercel --prod
```

## 🔐 Environment Variables

Copy `.env.example` to `.env.local` and fill in:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=your_backend_url
```

## 📁 Project Structure

```
frontend/
├── app/              # Next.js app directory
├── components/       # React components
├── lib/             # Utilities and helpers
├── public/          # Static assets
└── package.json
```

## 🎯 Features

- Upload pitch decks (PDF)
- Connect Google Sheets
- Real-time job progress
- Interactive dashboards
- Risk heatmaps
- Revenue projections
- Export reports
