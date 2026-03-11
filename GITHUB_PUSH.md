# 🔐 GitHub Push Instructions

## Step 1: Create GitHub Repository

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name**: `jee-rank-predictor`
   - **Description**: "JEE Rank Predictor with Gemini AI - Predicts JEE Main ranks with 97.8% accuracy"
   - **Public**: Yes (important for Render/Vercel to access)
   - **Add .gitignore**: No (we have it)
   - **Add README**: No (we have it)

3. Click **"Create repository"**

4. **Copy the HTTPS URL** it shows you

---

## Step 2: Connect Local Repo to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username and run:

```bash
cd "/Users/tejasavayadav/Desktop/jee rank pridictor"

git remote add origin https://github.com/YOUR_USERNAME/jee-rank-predictor.git

git branch -M main

git push -u origin main
```

### Example (if your username is `tejasavayadav`):

```bash
cd "/Users/tejasavayadav/Desktop/jee rank pridictor"

git remote add origin https://github.com/tejasavayadav/jee-rank-predictor.git

git branch -M main

git push -u origin main
```

---

## What Will Happen

1. **First command** connects your local git to GitHub
2. **Second command** ensures main branch is called "main"
3. **Third command** uploads all commits to GitHub

### Expected Output:

```
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Verify It Worked

Visit: `https://github.com/YOUR_USERNAME/jee-rank-predictor`

You should see:
- ✅ All your files uploaded
- ✅ 5 commits visible
- ✅ Code is ready for deployment

---

## Ready for Next Steps?

After this succeeds, you can:

1. **Deploy Backend** on Render (10 minutes)
2. **Deploy Frontend** on Vercel (5 minutes)
3. Share live links with users!

**Time from here to live deployment: ~20 minutes total**
