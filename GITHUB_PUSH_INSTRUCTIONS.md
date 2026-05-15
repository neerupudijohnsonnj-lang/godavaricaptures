# Push to GitHub - Step by Step Guide

Your Godavari Captures project is ready to push to GitHub! Follow these steps:

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon in top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `godavari-captures` (or your preferred name)
   - **Description**: "Luxury photography & reel-making studio website with instant booking"
   - **Visibility**: Choose **Private** or **Public**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Add GitHub Remote

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/godavari-captures.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Push to GitHub

```bash
git push -u origin master
```

This will push all your code to GitHub!

## Step 4: Verify Upload

1. Refresh your GitHub repository page
2. You should see all files uploaded
3. The README.md will display automatically

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Open GitHub Desktop
3. File → Add Local Repository → Select your project folder
4. Click "Publish repository" button
5. Choose visibility (Private/Public) and click "Publish"

## What's Included in Your Repository

✅ Complete frontend (React + Vite + Tailwind)
✅ Complete backend (FastAPI + Email service)
✅ All tests (15 property-based tests)
✅ Documentation (README, DEPLOYMENT, EMAIL_SETUP)
✅ Configuration files (.gitignore, requirements.txt, package.json)
✅ Spec files (.kiro/specs/)
✅ Images (hero background, portfolio images)

## What's NOT Included (Protected by .gitignore)

❌ `.env` file (sensitive credentials)
❌ `node_modules/` (dependencies)
❌ `__pycache__/` (Python cache)
❌ `.hypothesis/` (test cache)
❌ Build outputs

## After Pushing to GitHub

### Optional: Add Repository Description

On your GitHub repository page:
1. Click the ⚙️ gear icon next to "About"
2. Add description: "Luxury photography & reel-making studio website"
3. Add website URL (after deployment)
4. Add topics: `react`, `fastapi`, `photography`, `booking-system`, `tailwindcss`

### Optional: Add Repository Banner

1. Create a banner image (1280x640px recommended)
2. Upload to repository
3. Add to README: `![Banner](path/to/banner.png)`

### Optional: Enable GitHub Pages (for frontend only)

If you want to host the frontend on GitHub Pages:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: Select `master` → `/frontend/dist`
4. Build and deploy frontend first: `cd frontend && npm run build`

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/godavari-captures.git
```

### Error: "failed to push some refs"
```bash
git pull origin master --allow-unrelated-histories
git push -u origin master
```

### Error: Authentication failed
Use a Personal Access Token instead of password:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Use token as password when pushing

## Next Steps After GitHub Push

1. **Deploy Backend** - Use Railway, Render, or Heroku (see DEPLOYMENT.md)
2. **Deploy Frontend** - Use Netlify, Vercel, or GitHub Pages (see DEPLOYMENT.md)
3. **Set Environment Variables** - Add email credentials to deployment platform
4. **Update README** - Add live demo links after deployment
5. **Test Live Site** - Verify booking and email functionality

## Need Help?

- GitHub Docs: https://docs.github.com/en/get-started
- Contact: neerupudijohnsonnj@gmail.com

---

**Your repository is ready! Just create it on GitHub and push.** 🚀
