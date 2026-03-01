# Deployment Guide for Vercel

## Overview
This project consists of:
- **Frontend**: Static HTML/CSS/JS (Deploy to Vercel)
- **Backend**: Python Flask API (Deploy to Render, Railway, Heroku, etc.)

## Step 1: Deploy Backend

### Option A: Deploy to Render (Recommended)

1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `stock-portfolio-backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:create_app()`
5. Add Environment Variables:
   - Add any needed config variables (Flask will auto-load from `.env`)
6. Deploy

**Note your Backend URL**: e.g., `https://stock-portfolio-backend.onrender.com`

### Option B: Deploy to Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select repository
4. Railway auto-detects Python and deploys
5. Note your Backend URL in the Railway dashboard

### Option C: Deploy to Heroku

```bash
heroku create stock-portfolio-backend
git push heroku main
```

Note your Backend URL: `https://stock-portfolio-backend.herokuapp.com`

---

## Step 2: Deploy Frontend to Vercel

### Via GitHub (Easiest)

1. Push your code to GitHub
2. Go to https://vercel.com
3. Click "Import Project"
4. Connect GitHub and select your repository
5. **Configure Environment Variables**:
   - Click "Environment Variables"
   - Add variable: `VITE_BACKEND_URL` = Your backend URL from Step 1
   - Example: `https://stock-portfolio-backend.onrender.com`
6. Click Deploy

### Via CLI

```bash
npm install -g vercel
cd /path/to/Stock-Portfolio-Risk-Analyzer
vercel env add VITE_BACKEND_URL
# Enter your backend URL when prompted
vercel deploy
```

---

## Step 3: Verify Connection

1. Open your Vercel frontend URL
2. Use browser DevTools → Network tab
3. Click "Analyze" to trigger API calls
4. Verify API requests show `200 OK` responses

If you see `CORS errors` or `Failed to fetch`:
- Check backend URL is correct
- Ensure backend server is running
- Verify Backend has CORS enabled

---

## Environment Variables Reference

### Backend (Render/Railway/Heroku)
```
FLASK_ENV=production
FLASK_DEBUG=0
FRONTEND_URL=https://your-vercel-app.vercel.app  # Optional, for stricter CORS
```

### Frontend (Vercel)
```
VITE_BACKEND_URL=https://your-backend-app.onrender.com
```

---

## Troubleshooting

### "Cannot connect to backend"
- ✓ Check backend URL in Vercel environment variable
- ✓ Verify backend is running: `curl https://your-backend-url/api/health`
- ✓ Wait 30-60 seconds for Vercel build to complete

### CORS Errors
- ✓ Backend CORS is auto-configured for Vercel
- ✓ If custom origin, add to `FRONTEND_URL` env var in backend

### API Returns 5xx Errors
- Check Render/Railway/Heroku logs for backend errors
- Verify all Python dependencies are in `requirements.txt`

---

## Example Production URLs

**Frontend** (Vercel):
```
https://stock-portfolio.vercel.app
```

**Backend** (Render):
```
https://stock-portfolio-api.onrender.com
```

**Config for Frontend**:
```
VITE_BACKEND_URL=https://stock-portfolio-api.onrender.com
```

---

## Quick Deploy Commands

```bash
# 1. Deploy backend to Render
cd backend
render deploy

# 2. Deploy frontend to Vercel
vercel deploy --prod --env VITE_BACKEND_URL=https://your-backend-url.com

# 3. Test health check
curl https://your-backend-url.com/api/health
```

---

## Performance Tips

1. **Enable Caching**: Set `Cache-Control` headers in backend
2. **Use CDN**: Vercel automatically uses edge networks
3. **Optimize Images**: Frontend only uses text + charts
4. **Database**: If added, use managed PostgreSQL (keep it simple)

---

For questions, check the main README.md or GitHub issues.
