# 📤 How to Upload Your Quiz App to GitHub (No Technical Skills Required)

This guide will help you upload your quiz app to GitHub using only your web browser - no coding experience needed!

## Step 1: Create a GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up" if you don't have an account
3. Choose a username, email, and password
4. Verify your email address

## Step 2: Create a New Repository

1. Once logged in, click the green "New" button (or the "+" icon in the top right)
2. Fill in the repository details:
   - **Repository name**: `my-quiz-app` (or any name you prefer)
   - **Description**: "Interactive quiz application built with Streamlit"
   - Make sure it's set to **Public** (so others can access your deployed app)
   - ✅ Check "Add a README file"
3. Click "Create repository"

## Step 3: Upload Your Files

### Method A: Drag and Drop (Easiest)

1. Open your file explorer and navigate to the `streamlit-quiz-package` folder
2. Select ALL files in the folder:
   - app.py
   - questions.json
   - requirements.txt
   - Procfile
   - setup.sh
   - README.md
   - LICENSE
   - DEPLOYMENT.md
   - .streamlit folder (if visible)

3. In your GitHub repository page, click "uploading an existing file"
4. Drag and drop all the selected files into the upload area
5. Add a commit message like "Initial upload of quiz app"
6. Click "Commit changes"

### Method B: Upload One by One

1. In your GitHub repository, click "Add file" → "Upload files"
2. Click "choose your files" and select one file at a time:
   - Start with `app.py`
   - Then `questions.json`
   - Then `requirements.txt`
   - Continue with all other files
3. Add a commit message: "Upload quiz app files"
4. Click "Commit changes"

## Step 4: Deploy to Streamlit Cloud (Make it Live!)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub account
4. Click "New app"
5. Fill in the details:
   - **Repository**: Select your repository (e.g., `username/my-quiz-app`)
   - **Branch**: main
   - **Main file path**: `app.py`
6. Click "Deploy!"

## Step 5: Share Your App

1. Wait 2-3 minutes for deployment to complete
2. Your app will be available at: `https://username-my-quiz-app-main-app-abc123.streamlit.app`
3. Copy this URL and share it with anyone!

## 🎉 That's It!

Your quiz app is now live on the internet! Anyone can use it by clicking your link.

## Troubleshooting

### If deployment fails:
1. Check that all files were uploaded correctly
2. Make sure `requirements.txt` is present
3. Try redeploying from the Streamlit Cloud dashboard

### If you need to update questions:
1. Go to your GitHub repository
2. Click on `questions.json`
3. Click the pencil icon (Edit)
4. Make your changes
5. Click "Commit changes"
6. Your app will automatically update in 1-2 minutes!

### If you want to change the app title or appearance:
1. Edit the `app.py` file in GitHub (click pencil icon)
2. Look for the line with `st.title("🧠 Quiz App - Interactive Learning")`
3. Change the text between the quotes
4. Commit changes

## Need Help?

- Create an issue in your GitHub repository if something doesn't work
- The app automatically saves user statistics and allows question reporting
- Your app is now accessible worldwide! 🌍
