# Quick Start for Vercel Deployment

## TL;DR - 5 Minute Setup

### 1. **Deploy Backend** (Choose One)

**Render (Easiest):**
```bash
# Go to render.com → New Web Service
# Connect GitHub repo
# Build command: pip install -r requirements.txt
# Start command: gunicorn app:create_app()
# ➜ Note the URL: https://your-app.onrender.com
```

**Railway:**
```bash
# Go to railway.app → New Project
# Connect GitHub → Deploy
# ➜ URL shown in dashboard
```

### 2. **Deploy Frontend to Vercel**

**Option A - Via Vercel Dashboard (Recommended):**
```
1. Go to https://vercel.com
2. Import your GitHub repository
3. Add Environment Variable:
   - Name: VITE_BACKEND_URL
   - Value: https://your-backend-app.onrender.com
4. Click Deploy
```

**Option B - Via CLI:**
```bash
npm install -g vercel
cd your-project-folder
vercel env add VITE_BACKEND_URL
# Paste your backend URL when prompted
vercel deploy --prod
```

### 3. **Test the Connection**

1. Open your Vercel URL
2. Check browser console (F12) for connection status
3. You'll see: "✅ Connected" or "❌ Failed"

---

## Common Issues & Fixes

### Issue: "Cannot reach backend API"

**Solution:**
```
1. Check Backend URL is EXACTLY correct (copy-paste from Render/Railway)
2. Ensure it has https:// (not http://)
3. Add /api to the end if needed
4. Wait 30 seconds for Vercel rebuild
```

### Issue: CORS Errors

**Solution:**
- Backend already has CORS enabled
- Backend will auto-allow vercel.app domains

### Issue: After changing backend URL

**Solution:**
```
1. In Vercel: Go to Settings → Environment Variables
2. Update VITE_BACKEND_URL value
3. Redeploy project
4. Wait ~3 minutes
5. Refresh browser
```

---

## Environment Variables Cheat Sheet

| Where | Variable | Example |
|-------|----------|---------|
| Vercel Frontend | `VITE_BACKEND_URL` | `https://api.onrender.com` |
| Render Backend | `FRONTEND_URL` | `https://myapp.vercel.app` |
| Backend `.env` | None needed | (Auto-configured) |

---

## Verify Deployment Works

**Test Health Endpoint:**
```bash
curl https://your-backend-url.com/api/health
```

Should return:
```json
{
  "service": "Stock Portfolio Risk Analyzer API",
  "version": "1.0.0",
  ...
}
```

---

## Need Help?

1. **Check backend logs** (Render/Railway dashboard)
2. **Check frontend logs** (Vercel → Deployments → Logs)
3. **Browser console** (F12 → Console tab)
4. Check `DEPLOYMENT.md` for detailed guide

---

## Your URLs After Deploy

| Component | URL |
|-----------|-----|
| **Frontend** | `https://your-project.vercel.app` |
| **Backend API** | `https://your-backend.onrender.com` |
| **Health Check** | `https://your-backend.onrender.com/api/health` |

---

## Quick Reference Links

- Vercel Dashboard: https://vercel.com/dashboard
- Render Dashboard: https://dashboard.render.com
- Project Settings: In respective dashboards → Environment Variables
