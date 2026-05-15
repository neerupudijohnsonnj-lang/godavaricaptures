# Deploy Backend to Render - Quick Guide

## 🚨 Your booking form isn't working because the backend isn't deployed yet!

Follow these steps to deploy the backend and enable email notifications:

## Step 1: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Authorize Render to access your repositories

## Step 2: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Find and select your `godavaricaptures` repository
4. Click "Connect"

## Step 3: Configure the Service

Fill in these settings:

- **Name**: `godavari-backend`
- **Region**: Choose closest to India (Singapore recommended)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable" and add these 3 variables:

1. **SMTP_USER**
   - Value: `neerupudijohnsonnj@gmail.com`

2. **SMTP_PASSWORD**
   - Value: `thoo xomj exog xtqx`

3. **RECIPIENT_EMAIL**
   - Value: `neerupudijohnsonnj@gmail.com`

## Step 5: Deploy

1. Click "Create Web Service"
2. Wait 2-3 minutes for deployment
3. You'll get a URL like: `https://godavari-backend.onrender.com`
4. **Copy this URL!**

## Step 6: Connect Frontend to Backend

1. Go to https://vercel.com/dashboard
2. Find your `godavaricaptures` project
3. Click on it
4. Go to "Settings" → "Environment Variables"
5. Click "Add New"
6. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://godavari-backend.onrender.com` (your Render URL)
   - **Environment**: Select all (Production, Preview, Development)
7. Click "Save"

## Step 7: Redeploy Frontend

1. Go to "Deployments" tab in Vercel
2. Click "..." on the latest deployment
3. Click "Redeploy"
4. Wait 1-2 minutes

## ✅ Test It!

1. Go to your website: `https://godavaricaptures-urpx.vercel.app`
2. Fill out the booking form
3. Submit
4. Check your email: `neerupudijohnsonnj@gmail.com`
5. You should receive the booking details!

## 🎉 Done!

Your booking system is now fully functional with email notifications!

---

## ⚠️ Important Notes

- **Free tier**: Render free tier may sleep after 15 minutes of inactivity
- **First request**: May take 30-60 seconds to wake up
- **Upgrade**: Consider upgrading to paid tier ($7/month) for always-on service

## 🐛 Troubleshooting

**Backend not deploying?**
- Check build logs in Render dashboard
- Ensure `requirements.txt` exists in backend folder

**Still no emails?**
- Check Render logs for errors
- Verify SMTP credentials are correct
- Check spam folder

**Frontend still showing error?**
- Verify `VITE_API_URL` is set in Vercel
- Make sure you redeployed after adding the variable
- Check browser console for errors

---

**Need help? Contact: neerupudijohnsonnj@gmail.com**
