# Deployment Checklist - Save This!

## Pre-Deployment (Prepare)
- [ ] Repository pushed to GitHub with all latest code
- [ ] `backend/requirements.txt` contains all dependencies
- [ ] Tested locally with `python app.py`
- [ ] Frontend opens correctly in browser (http://127.0.0.1)

---

## Backend Deployment

### Using Render (Recommended)
- [ ] Account created at render.com
- [ ] GitHub connected to Render
- [ ] New Web Service created
- [ ] Python environment selected
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:create_app()`
- [ ] Service deployed successfully
- [ ] **Backend URL copied**: `https://_____.onrender.com`

### Alternative: Railway
- [ ] Account created at railway.app
- [ ] Project deployed from GitHub
- [ ] **URL noted**: `https://_____-railway.app`

### Alternative: Heroku
- [ ] Heroku CLI installed
- [ ] `heroku create stock-portfolio-api` executed
- [ ] Deployed with `git push heroku main`
- [ ] **URL noted**: `https://stock-portfolio-api.herokuapp.com`

---

## Frontend Deployment to Vercel

- [ ] Account created at vercel.com
- [ ] GitHub authorized with Vercel
- [ ] Project imported into Vercel
- [ ] Build detected (should be automatic)
- [ ] **Environment Variable Added:**
  - [ ] Name: `VITE_BACKEND_URL`
  - [ ] Value: `https://your-backend-url.com` (from previous step)
  - [ ] Saved successfully
- [ ] Frontend deployed successfully
- [ ] **Vercel URL copied**: `https://_____.vercel.app`

---

## Post-Deployment Verification

### Test Backend
- [ ] Opened: `https://your-backend-url.com/api/health` in browser
- [ ] Got JSON response (not error)
- [ ] Status shows `200 OK`

### Test Frontend
- [ ] Opened: `https://your-vercel-app.vercel.app`
- [ ] Page loaded successfully
- [ ] Debug panel visible (below header)
- [ ] Shows: **✅ Connected**

### Browser Console Check
- [ ] Opened F12 Developer Tools
- [ ] Went to Console tab
- [ ] Saw: `Backend URL: https://...`
- [ ] Saw: `✓ Backend connection successful!`

---

## Functionality Testing

- [ ] Added stock tickers (AAPL, MSFT, GOOGL)
- [ ] Clicked "Validate" button
- [ ] Saw confirmation message or errors listed
- [ ] Clicked "Analyze" button
- [ ] Dashboard loaded with metrics
- [ ] Tried other tabs:
  - [ ] Correlation (saw matrix)
  - [ ] Monte Carlo (can run simulation)
  - [ ] Scenario / Stress (can select scenarios)

---

## Troubleshooting Applied

- [ ] 
If Getting CORS Error:
  - [ ] Verified backend URL in Vercel env var
  - [ ] URL has https:// (not http://)
  - [ ] No trailing slash
  - [ ] Redeployed Vercel after fix

- [ ] If Backend 500 Error:
  - [ ] Checked Render/Railway logs
  - [ ] Verified Python dependencies installed
  - [ ] Waited 5 minutes (in case rate limit)

- [ ] If Still Getting Old URL:
  - [ ] Cleared browser cache (Cmd+Shift+R)
  - [ ] Tried incognito window
  - [ ] Waited 3 minutes for CDN

---

## Final Verification

- [ ] Frontend URL bookmarked: `https://_____.vercel.app`
- [ ] Backend URL for reference: `https://_____.onrender.com`
- [ ] App works end-to-end:
  - [ ] Add portfolio
  - [ ] Analyze
  - [ ] View results
- [ ] All tabs functional
- [ ] No console errors

---

## Success! 🎉

- [ ] Deployment complete
- [ ] App is live and working
- [ ] Share URL with users/team

---

## Notes

| Item | Value |
|------|-------|
| Frontend URL | https://_________________.vercel.app |
| Backend URL | https://_________________.onrender.com |
| Backend Health | https://_________________.onrender.com/api/health |
| Vercel Settings | Environment: VITE_BACKEND_URL |
| Date Deployed | _______________ |
| Issues (if any) | _______________ |

---

## Quick Contact Reference

- Vercel Support: https://vercel.com/support
- Render Support: https://render.com/docs
- GitHub Issues: [Your Repo]/issues

Keep this checklist after deployment for future reference!
