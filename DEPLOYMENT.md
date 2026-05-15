# Deployment Guide - Godavari Captures

## 🚀 Quick Deployment Options

### Option 1: GitHub Pages (Frontend Only - Static)
Not recommended as this requires a backend server.

### Option 2: Netlify + Railway (Recommended)

#### Frontend on Netlify
1. Push code to GitHub
2. Go to [Netlify](https://netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect your GitHub repository
5. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
6. Add environment variable:
   - `VITE_API_URL` = Your backend URL (from Railway)
7. Deploy!

#### Backend on Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root directory**: `backend`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   RECIPIENT_EMAIL=neerupudijohnsonnj@gmail.com
   ```
6. Deploy!
7. Copy the Railway URL and use it in Netlify's `VITE_API_URL`

### Option 3: Vercel + Render

#### Frontend on Vercel
1. Push to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your repository
4. Configure:
   - **Framework**: Vite
   - **Root directory**: `frontend`
   - **Build command**: `npm run build`
   - **Output directory**: `dist`
5. Add environment variable:
   - `VITE_API_URL` = Your backend URL
6. Deploy!

#### Backend on Render
1. Go to [Render](https://render.com)
2. New → Web Service
3. Connect your repository
4. Configure:
   - **Root directory**: `backend`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Deploy!

## 📝 Pre-Deployment Checklist

### Frontend
- [ ] Update API URL in production
- [ ] Test responsive design
- [ ] Optimize images
- [ ] Test all forms
- [ ] Check mobile menu

### Backend
- [ ] Set up email credentials
- [ ] Configure CORS for production domain
- [ ] Test all API endpoints
- [ ] Set up MongoDB (if using)
- [ ] Configure environment variables

## 🔧 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.com
```

### Backend (.env)
```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
RECIPIENT_EMAIL=neerupudijohnsonnj@gmail.com

# MongoDB (Optional)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=godavari_captures

# CORS (Optional - for specific domains)
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## 🌐 Custom Domain Setup

### Netlify/Vercel
1. Go to Domain settings
2. Add custom domain
3. Update DNS records:
   - Type: `A` or `CNAME`
   - Name: `@` or `www`
   - Value: Provided by platform

### Railway/Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS:
   - Type: `CNAME`
   - Name: `api` or subdomain
   - Value: Provided by platform

## 📊 Monitoring

### Frontend
- Netlify Analytics (built-in)
- Google Analytics (add to index.html)

### Backend
- Railway/Render logs (built-in)
- Sentry for error tracking (optional)

## 🔒 Security Checklist

- [ ] HTTPS enabled (automatic on most platforms)
- [ ] Environment variables secured
- [ ] CORS configured properly
- [ ] Rate limiting enabled (optional)
- [ ] Input validation working
- [ ] Email credentials using App Password

## 🚨 Troubleshooting

### Frontend not connecting to backend
- Check CORS configuration
- Verify API URL is correct
- Check browser console for errors

### Email not sending
- Verify Gmail App Password
- Check SMTP credentials
- Review backend logs

### Images not loading
- Ensure images are in `frontend/public/images/`
- Check image paths are correct
- Verify build includes public folder

## 📱 Testing Production

1. Test on multiple devices
2. Check all forms submit correctly
3. Verify email notifications work
4. Test mobile responsiveness
5. Check all navigation links
6. Test portfolio filtering

## 💰 Cost Estimate

### Free Tier (Recommended for start)
- **Netlify**: Free (100GB bandwidth)
- **Railway**: $5/month (500 hours)
- **Vercel**: Free (100GB bandwidth)
- **Render**: Free (750 hours)

### Paid Tier (For production)
- **Netlify Pro**: $19/month
- **Railway Pro**: $20/month
- **Vercel Pro**: $20/month
- **Render**: $7/month

## 🎯 Post-Deployment

1. Update README with live URLs
2. Test all functionality
3. Set up monitoring
4. Configure backups (if using MongoDB)
5. Share with client!

## 📞 Support

For deployment issues, contact: neerupudijohnsonnj@gmail.com

---

**Ready to deploy? Follow the steps above and your website will be live!** 🚀
