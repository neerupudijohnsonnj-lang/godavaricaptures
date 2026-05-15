# Deploy to Vercel - Complete Guide

## 🚀 Quick Deploy (Recommended)

### Step 1: Sign Up / Login to Vercel
1. Go to https://vercel.com
2. Click "Sign Up" or "Login"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### Step 2: Import Your Repository
1. Click "Add New..." → "Project"
2. Find and select `godavaricaptures` repository
3. Click "Import"

### Step 3: Configure Project Settings

**Framework Preset**: Vite
**Root Directory**: `frontend`
**Build Command**: `npm run build`
**Output Directory**: `dist`
**Install Command**: `npm install`

### Step 4: Deploy Frontend
Click "Deploy" - Vercel will build and deploy your frontend automatically!

Your frontend will be live at: `https://godavaricaptures.vercel.app` (or similar)

---

## 🔧 Backend Deployment (Required for Booking System)

Your frontend is now live, but you need to deploy the backend separately for the booking system to work.

### Option A: Deploy Backend on Render (Recommended)

1. Go to https://render.com
2. Sign up/login with GitHub
3. Click "New +" → "Web Service"
4. Connect your `godavaricaptures` repository
5. Configure:
   - **Name**: `godavari-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `SMTP_USER` = `neerupudijohnsonnj@gmail.com`
   - `SMTP_PASSWORD` = `thoo xomj exog xtqx`
   - `RECIPIENT_EMAIL` = `neerupudijohnsonnj@gmail.com`
7. Click "Create Web Service"

Your backend will be live at: `https://godavari-backend.onrender.com`

### Option B: Deploy Backend on Railway

1. Go to https://railway.app
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `godavaricaptures`
5. Add environment variables (same as above)
6. Railway will auto-detect Python and deploy

---

## 🔗 Connect Frontend to Backend

After deploying the backend, you need to update the frontend to use the production API URL.

### Update Vercel Environment Variable

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Add new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://godavari-backend.onrender.com` (or your Railway URL)
   - **Environment**: Production, Preview, Development (select all)
4. Click "Save"
5. Go to "Deployments" tab
6. Click "..." on latest deployment → "Redeploy"

---

## ✅ Verify Deployment

### Test Frontend
1. Visit your Vercel URL: `https://godavaricaptures.vercel.app`
2. Check that all sections load correctly
3. Verify images display properly

### Test Booking System
1. Fill out the "Book Instantly" form
2. Submit the form
3. Check if you receive an email at `neerupudijohnsonnj@gmail.com`
4. If email arrives, everything is working! 🎉

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem**: Images not loading
- **Solution**: Check that images are in `frontend/public/images/`
- Vercel serves files from `public/` at the root URL

**Problem**: Blank page
- **Solution**: Check Vercel build logs for errors
- Ensure all dependencies are in `package.json`

### Backend Issues

**Problem**: Booking form shows error
- **Solution**: Check backend logs on Render/Railway
- Verify `VITE_API_URL` is set correctly in Vercel
- Ensure backend URL is accessible (visit it in browser)

**Problem**: No email received
- **Solution**: Check backend logs for email errors
- Verify SMTP credentials are correct
- Check spam folder

### CORS Issues

**Problem**: "CORS policy" error in browser console
- **Solution**: Backend already has CORS enabled for all origins
- If issue persists, check backend logs

---

## 📊 Deployment Summary

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Vercel | `https://godavaricaptures.vercel.app` |
| Backend | Render/Railway | `https://godavari-backend.onrender.com` |
| Repository | GitHub | `https://github.com/neerupudijohnsonnj-lang/godavaricaptures` |

---

## 🔄 Future Updates

When you make changes to your code:

1. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```

2. **Automatic deployment**:
   - Vercel automatically redeploys frontend on push
   - Render/Railway automatically redeploys backend on push

---

## 💰 Pricing

- **Vercel**: Free tier (perfect for this project)
- **Render**: Free tier with 750 hours/month (backend may sleep after inactivity)
- **Railway**: $5/month credit (free trial available)

**Recommendation**: Use Vercel (frontend) + Render (backend) for completely free hosting!

---

## 📞 Need Help?

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Contact: neerupudijohnsonnj@gmail.com

---

**Your website is ready to go live! Follow the steps above and you'll be online in minutes.** 🚀
