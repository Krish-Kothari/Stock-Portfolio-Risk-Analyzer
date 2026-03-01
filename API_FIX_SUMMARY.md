# Vercel API Connection - FIXES APPLIED

## Problem
When deploying to Vercel, the frontend couldn't connect to the backend API because:
- Backend URL was hardcoded to `http://127.0.0.1:5000` (localhost only)
- No environment variable support for production
- No error handling for connection failures
- CORS wasn't explicitly configured for production

## Solutions Applied

### 1. ✅ **Dynamic Backend URL Configuration** 
**File**: `config.js` (NEW)
- Reads `VITE_BACKEND_URL` environment variable
- Falls back to localStorage for user customization
- Defaults to localhost for development
- Logs current URL for debugging

### 2. ✅ **Environment Variable Support**
**Files**: `vercel.json`, `.env.local`, `.env.example`
- Set backend URL via Vercel environment variables
- Works with Render, Railway, Heroku, or any backend

### 3. ✅ **Enhanced Error Messages**
**File**: `index.html` (Updated API helpers)
- Detailed CORS error messages
- Backend connection status shown on page
- Debug panel shows current API configuration
- Helpful troubleshooting text

### 4. ✅ **Better CORS Configuration**
**File**: `backend/app.py` (Updated CORS)
- Explicitly allows Vercel domains (`*.vercel.app`)
- Supports multiple origins: localhost, Vercel, custom domains
- Allows credentials for authenticated requests

### 5. ✅ **Debug UI Component**
**File**: `index.html` (Added debug panel)
- Shows current backend URL on page
- Shows connection status (✅ or ❌)
- Hidden in production (visible only on localhost)

---

## Files Changed/Created

### New Files:
```
✨ config.js                    - Backend URL configuration
✨ vercel.json                  - Vercel deployment config
✨ .env.example                 - Environment variables template
✨ .env.local                   - Local development config
✨ DEPLOYMENT.md                - Complete deployment guide
✨ VERCEL_QUICK_START.md        - 5-minute quick start
```

### Modified Files:
```
📝 index.html                   - Updated API helpers + debug UI
📝 backend/app.py               - Enhanced CORS configuration
```

---

## How to Deploy to Vercel

### Step 1: Deploy Backend
Choose one:
- **Render**: render.com → New → Python → Deploy
- **Railway**: railway.app → New Project → Deploy
- **Heroku**: `heroku create` + `git push heroku`

**Example (Render)**:
```
Service Name: stock-portfolio-api
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:create_app()
→ Note the URL: https://stock-portfolio-api.onrender.com
```

### Step 2: Deploy Frontend
1. Go to vercel.com
2. Import GitHub repository
3. **Add Environment Variable:**
   - Name: `VITE_BACKEND_URL`
   - Value: `https://stock-portfolio-api.onrender.com` (your backend URL)
4. Deploy

### Step 3: Verify
- Open your Vercel app
- Check bottom of page for "✅ Connected" or "❌ Failed"
- Console (F12) shows connection details

---

## Configuration Priority

The app looks for backend URL in this order:
1. `VITE_BACKEND_URL` environment variable (Vercel) ← **Use this**
2. `window.BACKEND_URL_OVERRIDE` (runtime override)
3. `localStorage.BACKEND_URL` (user customization)
4. `http://127.0.0.1:5000` (development default)

---

## Testing Locally First

Before deploying, test with local backend:

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Runs on http://127.0.0.1:5000

# Terminal 2: Open in browser
open index.html
# You'll see: ✅ Connected
```

---

## Production URLs Example

After deployment, your URLs will be:

```
Frontend (Vercel):
https://stock-portfolio.vercel.app

Backend (Render):
https://stock-portfolio-api.onrender.com

Health Check:
curl https://stock-portfolio-api.onrender.com/api/health
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot reach backend API" | Check VITE_BACKEND_URL env var in Vercel |
| CORS Error | Verify backend URL is correct (include https://) |
| "Backend URL not configured" | Add VITE_BACKEND_URL to Vercel environment |
| API returns 500 | Check backend logs in Render/Railway/Heroku |
| Changes not reflected | Redeploy Vercel after changing env var |

---

## Browser Console

When you open the app, check console (F12) for:

```
✓ Using Backend URL from environment variable: https://...
✓ Backend connection successful!

OR

❌ Cannot reach backend API. Make sure:
   1. Backend server is running
   2. Backend URL is correct: https://...
   3. CORS is enabled
```

---

## Next Steps

1. ✅ Deploy backend to Render/Railway
2. ✅ Note the backend URL
3. ✅ Deploy frontend to Vercel with `VITE_BACKEND_URL` env var
4. ✅ Open app URL and verify connection
5. ✅ Use the app!

For detailed instructions, see:
- `VERCEL_QUICK_START.md` - 5-minute guide
- `DEPLOYMENT.md` - Complete guide with all options
